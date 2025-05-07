const mysql = require('mysql2');

const pool = mysql.createPool({
    host: process.env.DB_HOST,
    user: process.env.DB_USER,
    database: process.env.DB_NAME,
    password: process.env.DB_PASSWORD, 
    waitForConnections: true,
    connectionLimit: 10,
    port: 3306,
    maxIdle: 5,
    idleTimeout: 60000,
    queueLimit: 2,
    enableKeepAlive: true,
    keepAliveInitialDelay: 0,
});

module.exports = {
    pool: pool
}