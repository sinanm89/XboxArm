var keystone = require('keystone');

var Rpis = keystone.list('Raspberry');

/**
 * List rpis
 */
exports.list = function(req, res) {
  Rpis.model.find(function(err, items) {

    if (err) return res.json({ err: err });

    res.json({
      rpis: items
    });

  });
}

/**
 * Get rpi by ID
 */
exports.get = function(req, res) {
  Rpis.model.findById(req.params.id).exec(function(err, item) {

    if (err) return res.json({ err: err });
    if (!item) return res.json('not found');

    res.json({
      rpi: item
    });

  });
}


/**
 * Create a rpi
 */
exports.create = function(req, res) {

  var item = new Raspberry.model(),
    data = (req.method == 'POST') ? req.body : req.query;

  item.getUpdateHandler(req).process(data, function(err) {

    if (err) return res.json({ error: err });

    res.json({
      rpi: item
    });

  });
}

/**
 * Patch rpi by ID
 */
exports.update = function(req, res) {

  Rpis.model.findById(req.params.id).exec(function(err, item) {

    if (err) return res.json({ err: err });
    if (!item) return res.json({ err: 'not found' });

    var data = (req.method == 'PUT') ? req.body : req.query;

    item.getUpdateHandler(req).process(data, function(err) {

      if (err) return res.json({ err: err });

      res.json({
        rpi: item
      });

    });

  });
}

// /**
//  * Delete People by ID
//  */
// exports.remove = function(req, res) {
//   People.model.findById(req.params.id).exec(function (err, item) {

//     if (err) return res.json({ dberror: err });
//     if (!item) return res.json('not found');

//     item.remove(function (err) {
//       if (err) return res.json({ dberror: err });

//       return res.json({
//         success: true
//       });
//     });

//   });
// }
