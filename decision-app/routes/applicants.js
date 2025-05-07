var express = require('express');
var router = express.Router();
const applicantsService = require('../services/applicants');

/* GET home page. */
router.get('/', async function(req, res, next) {
  let applicants = await applicantsService.getAll();
  res.render('applicants/index', { title: 'Express', applicants: applicants });
});

router.get('/:id', async function(req, res, next) {
  applicant = await applicantsService.getById(req.params.id);
  res.render('applicants/applicant', { applicant: applicant });
});

module.exports = router;
