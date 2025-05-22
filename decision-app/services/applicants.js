const pool = require('../db/connection').pool;
const GenericDB = require('./generic_db');

class ApplicantsService extends GenericDB {
    getByVacancyId = function(id) {
        return new Promise((resolve, reject) => {
            pool.query(`
                SELECT 
                    * 
                FROM vacancies_applicants va 
                    LEFT JOIN applicants a ON a.id = va.applicant_id
                WHERE 
                    vacancy_id = ?
                `, [id], (error, results) => {
                if (error) {
                    console.error('Error fetching applicants:', error);
                    return reject(error);
                }
                resolve(results);
            });
        });
    }

    getBestApplicants = function(id) {
        return new Promise((resolve, reject) => {
            pool.query(`
                select
                    a.*,
                    count(distinct at.token) as similar_tokens
                from
                    applicants_tokens at
                    inner join vacancies_tokens vt 
                        on vt.token = at.token and vt.vacancy_id = ?
                    inner join applicants a
                        on a.id = at.applicant_id
                group by 1
                HAVING similar_tokens > 2
                order by similar_tokens DESC 
                limit 50`,
                [id],
                (error, results) => {
                    if (error) {
                        console.error('Error fetching best applicants:', error);
                        return reject(error);
                    }
                    resolve(results);
                }
            )
        });
    }

    getApplicantsBySimilarityList = function(ids) {
        return new Promise((resolve, reject) => {
            let idMaps = {}
            ids = !ids?[]:ids;
            ids = ids.filter(i => i.score > 0.28);

            if(ids.length == 0) {
                resolve([]);
            }else{
                ids.forEach( i => {idMaps[i.id] = i.score});
                pool.query(`
                    select
                        a.*
                    from
                        applicants a
                    WHERE
                        id IN(?)
                    `,
                    [ids.map( i => i.id)],
                    (error, results) => {
                        if (error) {
                            console.error('Error fetching best applicants:', error);
                            return reject(error);
                        }

                        let sortedResult = results.sort( (a,b) => idMaps[b.id] - idMaps[a.id] );
                        //sortedResult.map( i=> console.log(`{${i.id} : ${idMaps[i.id]}}`));
                        resolve(sortedResult);
                    }
                );
            }
        });
    }
}

module.exports = new ApplicantsService('applicants');