var express = require('express');
var router = express.Router();
const vacancyService = require('../services/vacancies');
const applicantsService = require('../services/applicants');
const api = require('../api/parameters');

/* GET users listing. */
router.get('/', async function(req, res, next) {
  let pagination = new api.Pagination(req.query.pg, req.query.ps)
  let vacancies = await vacancyService.listVacanciesWithApplicantsCount(pagination);
  pagination.setTotalItems(vacancies.totalItems);
  res.render('vacancies/index', { title: 'Vagas', vacancies: vacancies.results, pagination: pagination });
});

router.get('/:id', async function(req, res, next) {
  let vacancy = await vacancyService.getById(req.params.id);
  let applicants = await applicantsService.getByVacancyId(vacancy.id);
  //let bestApplicants = await applicantsService.getBestApplicants(vacancy.id);
  //res.render('vacancies/vacancy', { vacancy: vacancy, applicants: applicants, bestApplicants: bestApplicants });
  res.render('vacancies/vacancy', { vacancy: vacancy, applicants: applicants });
});

module.exports = router;
