# 定时任务
class JobConfig(object):
    # SCHEDULER_API_ENABLED = True
    JOBS = [
            #  每7秒轮询节点列表
            {
                'id': 'store_data', # 任务唯一ID
                'func': 'app.jobs.job_store_data:store_data', # 执行任务的function名称，app.test 就是 app下面的`test.py` 文件，`shishi` 是方法名称。文件模块和方法之间用冒号":"，而不是用英文的"."
                'args': (), ##创建一把同步锁
                'trigger': 'cron',  # interval表示循环任务
                'second': '*/7',
            },
            # 每20秒判断一次节点是否脱离
            {
                'id': 'is_out',  # 任务唯一ID
                'func': 'app.jobs.job_store_data:is_out',
                # 执行任务的function名称，app.test 就是 app下面的`test.py` 文件，`shishi` 是方法名称。文件模块和方法之间用冒号":"，而不是用英文的"."
                'args': None,  # 如果function需要参数，就在这里添加
                'trigger': 'interval',  # interval表示循环任务
                'seconds': 60
            }
    ]