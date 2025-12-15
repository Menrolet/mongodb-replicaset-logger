try {
  const status = rs.status();
  if (status && status.ok === 1) {
    print("Replica set already initialized");
    quit(0);
  }
} catch (e) {
  print("rs.status() not available yet, initiating replica set...");
}

rs.initiate({
  _id: "rs0",
  members: [
    { _id: 0, host: "mongo1:27017" },
    { _id: 1, host: "mongo2:27017" },
    { _id: 2, host: "mongo3:27017" },
  ],
});
