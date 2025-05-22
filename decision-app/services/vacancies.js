const pool = require('../db/connection').pool;
const GenericDB = require('./generic_db');

class VacancyService extends GenericDB {
    listVacanciesWithApplicantsCountAndQuery = function(pagination, query) {
        return new Promise((resolve, reject) => {
            pool.query(`
                SELECT 
                    v.*, 
                    va.applicants
                FROM vacancies v
                LEFT JOIN 
                    (SELECT vacancy_id, count(distinct applicant_id) as applicants 
                        FROM vacancies_applicants GROUP BY 1) as va
                    ON va.vacancy_id = v.id
                WHERE
                    LOWER(v.title) like ?
                ORDER BY v.id desc
                LIMIT ?,?
            `, [`%${query}%`, pagination.getOffset(), pagination.pageSize], (error, results) => {
                if (error) {
                    console.error('Error fetching vacancies:', error);
                    reject(error);
                }

                pool.query('SELECT COUNT(1) AS total FROM vacancies', (error, countResults) =>{
                    if(error) {
                        console.error('Error fetching vacancies:', error);
                        reject(error);
                    }
                    resolve({results: results, totalItems: countResults[0].total});
                })
            });
        });
    }

    listVacanciesWithApplicantsCount = function(pagination) {
        return new Promise((resolve, reject) => {
            pool.query(`
                SELECT 
                    v.*, 
                    va.applicants
                FROM vacancies v
                LEFT JOIN 
                    (SELECT vacancy_id, count(distinct applicant_id) as applicants 
                        FROM vacancies_applicants GROUP BY 1) as va
                    ON va.vacancy_id = v.id
                ORDER BY v.id desc
                LIMIT ?,?
            `, [pagination.getOffset(), pagination.pageSize], (error, results) => {
                if (error) {
                    console.error('Error fetching vacancies:', error);
                    reject(error);
                }

                pool.query('SELECT COUNT(1) AS total FROM vacancies', (error, countResults) =>{
                    if(error) {
                        console.error('Error fetching vacancies:', error);
                        reject(error);
                    }
                    resolve({results: results, totalItems: countResults[0].total});
                })
            });
        });
    }
}

module.exports = new VacancyService('vacancies');