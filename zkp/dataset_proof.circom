pragma circom 2.0.0;

template DatasetCommitment() {
    signal input secret_dataset_chunk;
    signal input expected_hash;

    signal temp1;
    temp1 <== secret_dataset_chunk * secret_dataset_chunk;
    
    signal temp2;
    temp2 <== temp1 * secret_dataset_chunk;
    
    expected_hash === temp2 + secret_dataset_chunk;
}

component main {public [expected_hash]} = DatasetCommitment();
