const pool = require('../db/connection').pool;
const GenericDB = require('./generic_db');

class VacancyService extends GenericDB {
    listVacanciesWithApplicantsCount = function() {
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
                LIMIT ${this.defaultLimit}
            `, (error, results) => {
                if (error) {
                    console.error('Error fetching vacancies:', error);
                    return reject(error);
                }
                resolve(results);
            });
        });
    }
}

module.exports = new VacancyService('vacancies');