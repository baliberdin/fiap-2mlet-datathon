var express = require('express');
var router = express.Router();
const vacancyService = require('../services/vacancies');
const applicantsService = require('../services/applicants');
const api = require('../api/parameters');
const similarityService = require('../services/similarity');

/* GET users listing. */
router.get('/', async function(req, res, next) {
  let pagination = new api.Pagination(req.query.pg, req.query.ps, 0, req.query.q)
  let vacancies = []

  if(pagination.query) {
     vacancies = await vacancyService.listVacanciesWithApplicantsCountAndQuery(pagination, pagination.query);
  }else{
    vacancies = await vacancyService.listVacanciesWithApplicantsCount(pagination);
  }
  
  pagination.setTotalItems(vacancies.totalItems);
  res.render('vacancies/index', { title: 'Vagas', vacancies: vacancies.results, pagination: pagination });
});

router.get('/new', function(req, res, next){
  res.render('vacancies/new');
});

router.get('/:id', async function(req, res, next) {
  let vacancy = await vacancyService.getById(req.params.id);
  let applicants = await applicantsService.getByVacancyId(vacancy.id);
  let bestApplicants = await applicantsService.getBestApplicants(vacancy.id);

  applicantsSimilarityIds = await similarityService.getSimilarApplicants(vacancy.id);
  similarApplicants = await applicantsService.getApplicantsBySimilarityList(applicantsSimilarityIds);
  res.render('vacancies/vacancy', { vacancy: vacancy, applicants: applicants, similarApplicants:similarApplicants, bestApplicants: bestApplicants });
});

router.post('/', async function(req, res, next){
  let vacancy = {
    title: req.body.title,
    main_activities: req.body.main_activities,
    behavioral_skills: req.body.behavioral_skills,
    state: req.body.location.split(",")[0],
    city: req.body.location.split(",")[1],
    professional_level: req.body.professional_level,
    only_pwd: req.body.only_pwd != undefined,
    client: req.body.client,
    requested_date: new Date().toISOString("pt-BR").split("T")[0],
    objective: "Contratação",
    country: "Brasil"
  }

  let savedVacancy = await vacancyService.save(vacancy);
  vacancy.id = savedVacancy;
  similarityService.index(vacancy);
  res.redirect(`/vacancies/${savedVacancy}`);
});



module.exports = router;