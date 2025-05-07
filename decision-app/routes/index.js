var express = require('express');
var router = express.Router();
const vacancyService = require('../services/vacancies');

/* GET home page. */
router.get('/', async function(req, res, next) {
  let vacancies = await vacancyService.getAll();
  res.render('index', { title: 'Express', vacancies: vacancies });
});

module.exports = router;
