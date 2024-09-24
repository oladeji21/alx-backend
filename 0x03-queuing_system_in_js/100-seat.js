import { createClient } from 'redis';
import { createQueue } from 'kue';
import { promisify } from 'util';
import express from 'express';

// create redis client
const client = createClient();
const getAsync = promisify(client.get).bind(client);
let reservationEnabled;


function reserveSeat(number) {
  client.set('available_seats', number);
}

async function getCurrentAvailableSeats() {
  const availableSeats = await getAsync('available_seats');
  return availableSeats;
}

client.on('error', (error) => {
  console.log(`Redis client not connected to the server: ${error.message}`);
});

client.on('connect', () => {
  console.log('Redis client connected to the server');

  reserveSeat(50);
  reservationEnabled = true;
});

// creating Kue queue

const queue = createQueue();

// create express app

const app = express();
const port = 1245;

app.listen(port, () => {
  console.log(`app listening at http://localhost:${port}`);
});

app.get('/available_seats', async (req, res) => {
  const availableSeats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats: availableSeats });
});

app.get('/reserve_seat', (req, res) => {
  if (reservationEnabled === false) {
    res.json({ status: 'Reservation are blocked' });
    return;
  }

  const jobFormat = {};

  const job = queue.create('reserve_seat', jobFormat).save((err) => {
    if (err) {
      res.json({ status: 'Reservation failed' });
    } else {
      res.json({ status: 'Reservation in process' });
    }
  });

  job.on('complete', () => {
    console.log(`Seat reservation job ${job.id} completed`);
  });

  job.on('failed', (errorMessage) => {
    console.log(`Seat reservation job ${job.id} failed: ${errorMessage}`);
  });
});

app.get('/process', async (req, res) => {
  queue.process('reserve_seat', async (job, done) => {
    let availableSeats = await getCurrentAvailableSeats();

    if (availableSeats <= 0) {
      done(Error('Not enough seats available'));
    }

    availableSeats = Number(availableSeats) - 1;

    reserveSeat(availableSeats);

    if (availableSeats <= 0) {
      reservationEnabled = false;
    }

    done();
  });
  res.json({ status: 'Queue processing' });
});
