var keystone = require('keystone');

exports = module.exports = function (req, res) {

  var view = new keystone.View(req, res);
  var locals = res.locals;

  // Set locals
  locals.section = 'register_rpi';
  locals.filters = {
    post: req.params.page,
  };
  locals.data = {
    rpis: [],
  };

  // Load the current post
  view.on('init', function (next) {

    var q = keystone.list('Page').model.find();

    q.exec(function (err, result) {
      locals.data.rpis = result;
      next(err);
    });

  });

  // Render the view
  view.render('page');
};
