To prepare a model:
1. Open console.
2. Open a python file train.py
3. Choose directory with txt files for training by passing --input-dir argument
in console. If argument is None, training will be implemented from stdin.
4. Use --model to define path to file with train model(it will be created if
there is no such file)
5. Wait a bit
(6. --lc will make text lower case)

To generate text:
1. Open a console.
2. Open a python file generate.py.
3. Choose file for existing training model by passing --model argument.
4. Use --output to define dir(not strict) and it is necessary to limit the
generated word sequence by --length 'some integer number'
5. Wait a bit