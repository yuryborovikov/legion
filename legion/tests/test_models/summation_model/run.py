import legion.model
import legion.k8s

legion.model.init('test summation', '1.0')

<<<<<<< 63cede55a3f38705615175ecc6d66e2c7d8a7bcc
# py_model.properties['prop_1'] = 0.6
# py_model.on_property_change(lambda key: print(key))
=======
py_model = legion.pymodel.Model('test summation', '1.0')  # do the same shit as model.init does
                                                          # and set legion.model.context

import configparser
cm = configparser.ConfigParser()


get('key', cast=int)


py_model.define_property('prop_1', 0.5)  # start-value is required
# py_model.properties['prop_1'] = 0.5 ^^^^^^^^  (just initialization)


py_model.on_property_change(lambda key: print(key))

py_model.send_metrics('metric_a', 1.0)
>>>>>>> [#250] Update typing system, add tests

secret_storage = K8SPropertyStorage('NAMEPSPACE', 'NAME')

download_from_s3(sk_id=secret_storage['key1'])

def calculate(x):
    # a = legion.model.properties['prop_1']
    return int(x['a']) + int(x['b'])


calculate({'a': 1.0, 'b': 20.1})

legion.model.export_untyped(lambda x: {'result': int(calculate(x))})
legion.model.save('abc.model')
