from easydict import EasyDict

exp_args = dict(
    data=dict(
        dataset='tiny_imagenet',
        data_path='./data/tiny-imagenet-200',
        sample_method=dict(name='dirichlet', alpha=0.2, train_num=500, test_num=100)
    ),
    learn=dict(
        device='cuda:0',
        local_eps=8,
        global_eps=40,
        batch_size=32,
        optimizer=dict(name='sgd', lr=0.02, momentum=0.9),
        # Only fine-tune parameters whose name contain the keyword "fedrod_p_head".
        finetune_parameters=dict(name='contain', keywords=['fedrod_p_head']),
    ),
    model=dict(
        name='fedrod_resnet8',
        input_channel=3,
        class_number=200,
    ),
    client=dict(name='fedrod_client', client_num=40),
    server=dict(name='base_server'),
    group=dict(
        name='base_group',
        aggregation_method='avg',
        # Only aggregate parameters whose name does not contain the keyword "fedrod_p_head".
        aggregation_parameters=dict(
            name='except',
            keywords=['fedrod_p_head'],
        ),
    ),
    other=dict(test_freq=3, logging_path='./logging/tiny_imagenet_fedrod_resnet_dirichlet_02')
)

exp_args = EasyDict(exp_args)

if __name__ == '__main__':
    from fling.pipeline import personalized_model_pipeline

    personalized_model_pipeline(exp_args, seed=0)
