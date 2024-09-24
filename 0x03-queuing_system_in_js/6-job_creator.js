import kue from 'kue';

const queue = kue.createQueue();

const jobPayload = {
  phoneNumber: '4153518780',
  message: 'This is the code to verify your account',
};

const queueName = 'push_notification_code';

const job = queue.create(queueName, jobPayload).save((err) => {
  if (!err) console.log(`Notification job created: ${job.id}`);
});

job.on('complete', () => {
  console.log('Notification job completed');
});

job.on('failed', () => {
  console.log('Notification job failed');
});
