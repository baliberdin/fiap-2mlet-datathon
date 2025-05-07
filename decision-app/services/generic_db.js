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
};