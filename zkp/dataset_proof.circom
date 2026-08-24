pragma circom 2.0.0;

template Num2Bits(n) {
    signal input in;
    signal output out[n];
    var lc1=0;
    var e2=1;
    for (var i = 0; i<n; i++) {
        out[i] <-- (in >> i) & 1;
        out[i] * (out[i] -1 ) === 0;
        lc1 += out[i] * e2;
        e2 = e2 + e2;
    }
    lc1 === in;
}

template LessThan(n) {
    signal input in[2];
    signal output out;
    component n2b = Num2Bits(n+1);
    n2b.in <== in[0] + (1<<n) - in[1];
    out <== 1-n2b.out[n];
}

template DatasetCommitment() {
    // Existing identity verification
    signal input secret_dataset_chunk;
    signal input expected_hash;
    
    // New ZKML Range Constraint variables
    signal input weight_magnitude;
    signal input max_weight_magnitude;

    // 1. Verify Identity
    signal temp1;
    temp1 <== secret_dataset_chunk * secret_dataset_chunk;
    
    signal temp2;
    temp2 <== temp1 * secret_dataset_chunk;
    
    expected_hash === temp2 + secret_dataset_chunk;

    // 2. Verify Weight Update (ZKP catches poisoned/blown-up weights!)
    component lt = LessThan(60);
    lt.in[0] <== weight_magnitude;
    lt.in[1] <== max_weight_magnitude;
    lt.out === 1; 
}

component main {public [expected_hash, max_weight_magnitude]} = DatasetCommitment();
