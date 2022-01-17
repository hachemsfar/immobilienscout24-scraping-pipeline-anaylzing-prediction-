import Extract_Transform,Load
import logging

if __name__ == '__main__':
    logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

    # 1. Run Extract/Transform
    logging.info('# 1. Run Extract/Transform')
    new_ads=Extract_Transform.Extract_and_Transform()
    # 2. Run Load
    logging.info('# 1. Run Load')
    Load.load(new_ads)