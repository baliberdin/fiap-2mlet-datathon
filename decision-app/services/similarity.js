module.exports = {

    async getSimilarApplicants(vacancyId){
        let resource = `http://${process.env.SIMILARITY_API_HOST}:${process.env.SIMILARITY_API_PORT}/similarity/applicants?vacancy_id=${vacancyId}&limit=20`;
        console.log("Fetching: ", resource);
        return new Promise((resolve, reject) => {
            fetch(resource)
            .then( async response => {
                if(response.status != 200){
                    console.log(`Erro on similarity API call (status=${response.status}), returning an empty List.`);
                    resolve([]);
                }else{
                    let body = await response.json();
                    resolve(body.similar_documents);
                }
            })
            .catch(e => {
                console.log("Erro on similarity API call, returning an empty List.", e);
                resolve([]);
            });
        });
    },

    async index(vacancy){
        let resource = `http://${process.env.SIMILARITY_API_HOST}:${process.env.SIMILARITY_API_PORT}/document/vacancies`
        console.log(vacancy);
        let data = {
            id: vacancy.id,
            title: vacancy.title,
            description: (vacancy.main_activities?vacancy.main_activities:'') + '\n'+ (vacancy.technical_and_behavioral_skills?vacancy.technical_and_behavioral_skills:'') + '\n' + (vacancy.behavioral_skills?vacancy.behavioral_skills:'')    ,
            location: vacancy.state+', '+vacancy.city
        }
        const response = await fetch(resource, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
    }

}