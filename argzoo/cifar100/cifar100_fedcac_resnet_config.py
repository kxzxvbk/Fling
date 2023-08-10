from easydict import EasyDict
import argparse
def args_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--tau', type=float, default=0.4, help='tau')
    parser.add_argument('--beta', type=int, default=170, help='beta')
    parser.add_argument('--noniid', type=str, default='dirichlet', help='noniid type')
    parser.add_argument('--alpha', type=float, default=0.5, help='alpha')
    parser.add_argument('--seed', type=int, default=1, help='seed')
    args = parser.parse_args()
    args.alpha = args.alpha if args.noniid == 'dirichlet' else int(args.alpha)
    return args

args = args_parser()
tau = args.tau
beta = args.beta
noniid = args.noniid
alpha = args.alpha
seed = args.seed

exp_args = dict(
    data=dict(
        dataset='cifar100',
        data_path='./data/CIFAR100',
        sample_method=dict(name=noniid, alpha=alpha, train_num=500, test_num=100),
        transforms=dict(
            horizontal_flip=dict(p=0.5),
            random_rotation=dict(degree=15),
            to_tensor=dict(),
            Normalize=dict(mean=[0.507, 0.487, 0.441], std=[0.267, 0.256, 0.276]),
        ),
    ),
    learn=dict(
        device='cuda:0',
        local_eps=5,
        global_eps=300,
        batch_size=100,
        optimizer=dict(name='sgd', lr=0.1, momentum=0.9),
        finetune_parameters=dict(name='all'),
        test_place=['after_aggregation', 'before_aggregation'],
        tau=tau,   # the ratio of critical parameters in FedCAC
        beta=beta,   # used to control the collaboration of critical parameters
    ),
    model=dict(
        name='resnet10',
        input_channel=3,
        class_number=100,
    ),
    client=dict(name='fedcac_client', client_num=40),
    server=dict(name='base_server'),
    group=dict(
        name='fedcac_group',
        aggregation_method='avg',
        # Only aggregate parameters whose name does not contain the keyword "fc".
        aggregation_parameters=dict(name='all', ),
    ),
    other=dict(test_freq=1, logging_path=f'./logging/cifar100_fedcac_resnet/{noniid}_{alpha}/{tau}_{beta}/{seed}')
)

exp_args = EasyDict(exp_args)

if __name__ == '__main__':
    from fling.pipeline import personalized_model_pipeline

    personalized_model_pipeline(exp_args, seed=seed)
