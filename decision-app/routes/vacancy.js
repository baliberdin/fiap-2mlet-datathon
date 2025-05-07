var express = require('express');
var router = express.Router();
const vacancyService = require('../services/vacancies');
const applicantsService = require('../services/applicants');

/* GET users listing. */
router.get('/', async function(req, res, next) {
  let vacancies = await vacancyService.listVacanciesWithApplicantsCount();
    res.render('vacancies/index', { title: 'Vagas', vacancies: vacancies });
});

router.get('/:id', async function(req, res, next) {
  let vacancy = await vacancyService.getById(req.params.id);
  let applicants = await applicantsService.getByVacancyId(vacancy.id);
  let bestApplicants = await applicantsService.getBestApplicants(vacancy.id);
  res.render('vacancies/vacancy', { vacancy: vacancy, applicants: applicants, bestApplicants: bestApplicants });
});

module.exports = router;
