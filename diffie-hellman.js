//
// Diffie-Hellman is a way of generating a shared secret between two people in such a way that the secret can't be seen by observing the communication. That's an important distinction: You're not sharing information during the key exchange, you're creating a key together.

// This is particularly useful because you can use this technique to create an encryption key with someone, and then start encrypting your traffic with that key. And even if the traffic is recorded and later analyzed, there's absolutely no way to figure out what the key was, even though the exchanges that created it may have been visible. This is where perfect forward secrecy comes from. Nobody analyzing the traffic at a later date can break in because the key was never saved, never transmitted, and never made visible anywhere.

// The way it works is reasonably simple. A lot of the math is the same as you see in public key crypto in that a trapdoor function is used. And while the discrete logarithm problem is traditionally used (the xy mod p business), the general process can be modified to use elliptic curve cryptography as well.

// But even though it uses the same underlying principles as public key cryptography, this is not asymmetric cryptography because nothing is ever encrypted or decrypted during the exchange. It is, however, an essential building-block, and was in fact the base upon which asymmetric crypto was later built.

// The basic idea works like this:

// I come up with two prime numbers g and p and tell you what they are.
// You then pick a secret number (a), but you don't tell anyone. Instead you compute ga mod p and send that result back to me. (We'll call that A since it came from a).
// I do the same thing, but we'll call my secret number b and the computed number B. So I compute gb mod p and send you the result (called "B")
// Now, you take the number I sent you and do the exact same operation with it. So that's Ba mod p.
// I do the same operation with the result you sent me, so: Ab mod p.
// The "magic" here is that the answer I get at step 5 is the same number you got at step 4. Now it's not really magic, it's just math, and it comes down to a fancy property of modulo exponents. Specifically:

// (g^a mod p)^b mod p = g^(ab) mod p
// (g^b mod p)^a mod p = g^(ba) mod p

// node.js 0.5 Diffie-Hellman example
var assert = require("assert");
var crypto = require("crypto");

// the prime is shared by everyone
var server = crypto.createDiffieHellman(512);
var prime = server.getPrime();

// happening on server
// sharing secret key on a pair
var alice = crypto.createDiffieHellman(prime);
// alice picks a
var alicePub = alice.generateKeys();
// alices computed A
// alice shares A with bob

// happening on raspberry
var bob = crypto.createDiffieHellman(prime);
// bob pics b
var bobPub = bob.generateKeys();
// bobs computed B
// bob shares B with alice

var bobAliceSecret = bob.computeSecret(alicePub);
// g^(ba) mod p
var aliceBobSecret = alice.computeSecret(bobPub);
// g^(ab) mod p

// public keys are different, but secret is common.
assert.notEqual(bobPub, alicePub);
assert.equal(bobAliceSecret, aliceBobSecret);
// use common secret as shared encryption key...


// shared secret with 3rd person
var carol = crypto.createDiffieHellman(prime);
var carolPub = carol.generateKeys();

var carolAliceSecret = carol.computeSecret(alicePub);
var aliceCarolSecret = alice.computeSecret(carolPub);

assert.notEqual(carolPub, alicePub);
assert.equal(carolAliceSecret, aliceCarolSecret);

// secret depends on pairs
assert.notEqual(aliceBobSecret, aliceCarolSecret);
var carolBobSecret = carol.computeSecret(bobPub);
assert.notEqual(carolAliceSecret, carolBobSecret);

