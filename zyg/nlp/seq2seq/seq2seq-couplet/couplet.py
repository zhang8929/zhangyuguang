
from model import Model

m = Model(
        '/home/zhangyg/data/couplet/train/in.txt',
        '/home/zhangyg/shuju/data/couplet/train/out.txt',
        '/home/zhangyg/shuju/data/couplet/test/in.txt',
        '/home/zhangyg/shuju/data/couplet/test/out.txt',
        '/home/zhangyg/shuju/data/couplet/vocabs',
        num_units=1024, layers=4, dropout=0.2,
        batch_size=32, learning_rate=0.001,
        output_dir='/home/zhangyg/data/models/tf-lib/output_couplet',
        restore_model=False)

m.train(5000000)
