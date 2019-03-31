const concat = require('gulp-concat');
const gulp = require('gulp');
const path = require('path');
const rimraf = require('rimraf');
const strip = require('gulp-strip-comments');

const DIST_DIR = path.join(__dirname, 'dist');
const NODE_DIR = path.join(__dirname, 'node_modules');
const STATIC_DIR = path.join(__dirname, 'assets');
const VENDOR_DIR = path.join(STATIC_DIR, 'vendor');

const vendorCssPaths = [
  'bulma/css/bulma.min.css'
];

function clean() {
  return Promise.all([
    new Promise(resolve => rimraf(path.join(VENDOR_DIR, '**', '!(.keep)*'), resolve)),
    new Promise(resolve => rimraf(path.join(DIST_DIR, '**', '!(.keep)*'), resolve)),
  ]);
}

function vendorCss() {
  return gulp.src(vendorCssPaths.map(filepath => path.join(NODE_DIR, filepath)))
    .pipe(concat('vendor.css'))
    .pipe(gulp.dest(VENDOR_DIR));
}

const vendor = gulp.parallel(vendorCss);
const build = gulp.series(clean, vendor);

gulp.task('clean', clean);
gulp.task('vendor', vendor);
gulp.task('build', build);
