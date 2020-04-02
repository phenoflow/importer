const express = require('express');
const router = express.Router();
const logger = require('../config/winston');
const models = require('../models');
const config = require('config');
const request = require('request');

const Utils = require('../util/utils');

router.post('/new', function(req, res, next) {

  if (!req.body.author || !req.body.about) {
    res.sendStatus(500);
  } else {
    models.workflow.create({
      author: req.body.author,
      about: req.body.about
    }).then(
      (created)=>res.send({"id": created.id})
    );
  }

});

router.get("/generate/:workflowId/:language", async function(req, res, next) {

  let workflow = await models.workflow.findOne({
    where: {
      id: req.params.workflowId
    }
  });

  let steps = await models.step.findAll({
    where: {
      workflowId: req.params.workflowId
    }
  });

  let mergedSteps = [];

  for (const step in steps) {
    let mergedStep = JSON.parse(JSON.stringify(steps[step]));
    mergedStep.inputs = await models.input.findAll({
      where: {
        stepId: steps[step].id
      }
    });
    mergedStep.outputs = await models.output.findAll({
      where: {
        stepId: steps[step].id
      }
    });
    mergedStep.implementation = await models.implementation.findOne({
      where: {
        stepId: steps[step].id,
        language: req.params.language
      }
    });

    if (!mergedStep.implementation) {
      res.sendStatus(500);
      return;
    }

    mergedSteps.push(mergedStep);
  }

  request.post(config.get("generator.URL") + "/generate", {json: mergedSteps}, async function(error, response, data) {

    if(error && error.code=="ECONNREFUSED") {
      res.sendStatus(503);
      return;
    }
    if (!error && response.statusCode == 200) {
      await Utils.createPFZipResponse(res, req.params.workflowId, response.body.workflow, response.body.workflowInputs, req.params.language, response.body.steps, workflow.about);
    } else {
      res.sendStatus(500);
    }

  });

});

module.exports = router;
