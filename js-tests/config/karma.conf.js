basePath = '../..';

files = [
  JASMINE,
  JASMINE_ADAPTER,
  'spudblog/static/js/lib/underscore.js',
  'spudblog/static/js/lib/angular.js',
  'spudblog/static/js/lib/angular-*.js',
  'spudblog/static/js/spudblog/services.js',
  'spudblog/static/js/spudblog/app.js',
  'js-tests/lib/*.js',
  'js-tests/tests/*.js'
];

autoWatch = true;

browsers = ['Chrome'];

junitReporter = {
  outputFile: 'js-tests/test-out/unit.xml',
  suite: 'unit'
};