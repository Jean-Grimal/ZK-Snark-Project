# Proving knowledge of hash preimage with ZK-SNARK proofs on the Ethereum Blockchain


## Project Description

The goal of this project is the implementation of a tool allowing to emit Zk-Snarks proofs  of knowing the antecedent of a sha-256 hash, and to verify them on the Ethereum blockchain via a smart contract.

For that, I use the Zokrates toolbox, which works as follows:
We have to write a Zokrates file that describes the type of proof we want to manipulate (in our case: the knowledge of the presage of a sha-256).

Then, via bash commands, Zokrates uses this file to create a prooving key (allowing to emit the desired ZK-snark proofs) as well as a verificiation key and a smart contract which allow to verify these proofs. This smart contract will be deployed on the Ethereum Blockchain. Still with bash command Zokrates allows us to generate ZK-Snark proofs as json files.


We'll limit the hash preimages to strings as their size is limited.

## Prerequisites

You will need to install [truffle](https://trufflesuite.com//) and [ganache](https://trufflesuite.com/docs/ganache/quickstart/) as we'll use them to deploy and test the smart contracts.
You will also need to install [docker](https://www.docker.com/) to use the [zokrates](https://zokrates.github.io/) command lines.

Yoo will find all the files in the src folder of the repo.

## Zokrates files 


We don't need to implement the sha-256 function (already implemented in a .zok library), however, this implementation forces us to set the size of the antecedent of the hash we want to prove the knowledge of.

That's why I wrote 4 .zok files : they correspond to different sizes of hash pre-image.

There are only 4 of them because from a certain size, Zokrates can't compile the file anymore.

Here is an exemple of the zokrates files we will use :

```python
import "hashes/sha256/sha256" as sha256

def main(private u32[1][16] a) -> u32[8]:
    u32[8] h = sha256(a)
	return h
```

## Scripts explanations


### slicing.py
 takes a string as input. This string is the preimage of the hash.

The sha-256 function implemented on zokrates takes as argument u32 lists (to limit the size of the elements that will transit on the Blockchain) which corresponds to a precise cutting of an object (string in our case) written in binary form (this is the preliminary step of hashing an object, which is not implemented by zokrates).

Therefore this script implements the cutting of a string encoded in utf-8 into a list of u32 integers ready to be hashed.

This script gives 2 output : the cutting of the string and the name of the Zokrates file to use (based on the size of the preimage).

### bash scripts

The two others are bash scripts, automating the zokrates command lines.

These command lines should be written in the shell of a special Docker container obtained via the command:

```bash
docker run -ti zokrates/zokrates /bin/bash
```

You will then have to copy the zok files inside this container via the docker cp commands :

```bash
docker cp ./root.zok f97217423880:home/zokrates
```
(the container ID is obtained via the docker ps command)


- compile.sh : 

It aims to generate the trusted setup allowing to create proofs, and the smart contract allowing to verify them (it will be necessary to deploy this smart contract on a blockchain with the help of Ganache and Truffle). 

It takes takes as input : a .zok file, the name for the .zok file once compiled, and names for the proving key, verification key and verifier smart contract that will be generated.  Ex :

```bash
bash compile.sh get_hash1.zok get_hash1 prooving1.key verication1.key verifier1.sol
```

- proof.sh : 

This one is used to generate a proof of knowledge of the antecedent of a hash.

It takes as input a .zok file compiled corresponding to the type of proof desired (thus depending on the size of the antecedent), the antecedent of the hash (in the form of a list of U32, obtained via the python script) and the proving key. Ex : 

```bash
bash proof.sh get_hash1 '1248158062 541553257 1835101312 0 0 0 0 0 0 0 0 0 0 0 0 88' proving1.key
verifier1.sol
```
with '1248158062 541553257 1835101312 0 0 0 0 0 0 0 0 0 0 0 0 88' being the slicing of "Jean Grimal" given by slicing.py

Let’s take a look at the json file (the proof) generated : We recognize the hash (for which we want to prove the knowledge of the preimage) in the input section. 

## Proof verification via Truffle

(It could also be deployed on a Ethereum Blockchain testnet, or the mainnet but it would be very expensive because of gas fees, that's why we use Truffle)

### Preliminary steps:

- Launch Ganache
- Initialize a truffle project with the command : 
```bash
 truffle init
```
- In the migrations directory, don't forget to add the file 2_deploy contracts.js : 
```javascript
const verifier = artifacts.require("verifier");
 
module.exports = function(deployer) {
  deployer.deploy(verifier);
};
```

- Check that the version of solidity used by verifier.sol is the same as the one of truffle-config.js, if it is not the same, modify it so that it is the case.

- Add the verifier.sol in the contracts folder of the truffle project.

- Adapt the port (usually 7545), in the development section of truffle-config.js

- Then use these command lines to compile the smart contract and deploy it on the blockchain :

```bash
 truffle compile
 truffle migrate
```

### Verification

To proceed with the verification of the proof, from the truffle project, use the command lines :

```bash
truffle console
contract = await Verifier.new()
proof = JSON.parse(fs.readFileSync(\proof.json\))
await contract.verifyTx(proof.proof.a, proof.proof.b, proof.proof.c, proof.inputs)
```

If the proof is valid, the verifyTx function will return true. Otherwise, it will return false, or an error message.
