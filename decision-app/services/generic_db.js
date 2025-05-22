const pool = require('../db/connection').pool;

module.exports = class GenericDB {

    constructor(table) {
        this.table = table;
        this.defaultLimit = 100
    }

    getAll = function() {
        return new Promise((resolve, reject) => {
            pool.query(`SELECT * FROM ${this.table} order by id desc limit ${this.defaultLimit}`,  (error, results) => {
                if (error) {
                    return reject(error);
                }
                resolve(results);
            });
        });
    }

    getById = function(id) {
        return new Promise((resolve, reject) => {
            pool.query(`SELECT * FROM ${this.table} WHERE id = ?`, [id], (error, results) => {
                if (error) {
                    return reject(error);
                }
                resolve(results[0]);
            });
        });
    }

    save = function(obj) {
        return new Promise((resolve, reject) => {
            let keys = Object.keys(obj);
            let values = keys.map( k => obj[k]);
            //console.log(keys);
            //console.log(values);

            let stmt = `INSERT INTO ${this.table} (${keys.join(", ")}) VALUES(${keys.map( k => "?").join(",")})`;

            //console.log(stmt);
            pool.query(stmt, values, (error, results) => {
                if (error) {
                    return reject(error);
                }
                console.log(results);
                resolve(results.insertId);
            });
        });
    }
};
