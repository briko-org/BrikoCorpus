import argparse, random

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get random samples from the BrikoCorpus')
    parser.add_argument(
        '-num_samples',
        dest='num_samples',
        default=100,
        type=int,
        help='Number of samples to extract from the BrikoCorpus.',
    )
    parser.add_argument(
        '-corpus_path',
        dest='corpus_path',
        default='FinalContent.txt',
        type=str,
        help='Path to the BrikoCorpus.',
    )
    parser.add_argument(
        '-sample_path',
        dest='sample_path',
        default='SampleCorpus.txt',
        type=str,
        help='Path to the samples.',
    )
    args = parser.parse_args()

    with open(args.corpus_path,'r') as finalContent:
        lines = finalContent.read().splitlines()
        final_size = len(lines)
        randomList = random.sample(range(0,final_size - 1), args.num_samples)
        with open(args.sample_path,'w') as sampleCorpus:
            for i in randomList:
                sampleCorpus.write(lines[i] + '\n')

