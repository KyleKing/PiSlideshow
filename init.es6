#!/usr/bin/env node

// Raspberry Pi PhotoFrame
// by Kyle King

/**
 * General Configuration
 */
require('babel-register');
const fs = require('fs-extra');

const program = require('commander');
program
  .version(fs.readJsonSync('package.json'))
  .option('-d, --debug', 'run in debug mode (verbose)')
  .option('-l, --local', 'when not a Raspberry Pi, run in `local` mode')
  .parse(process.argv);
process.env.DEBUG = program.debug || false;
process.env.LOCAL = program.local || false;

const config = require('./modules/configure.es6');
const dbCloudDir = fs.readJsonSync('./secret.json').balloonDir;
config.init(dbCloudDir);
