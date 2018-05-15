package main

// This file is for the mining code.
// Note that "targetBits" for this assignment, at least initially, is 33.
// This could change during the assignment duration!  I will post if it does.

// Mine mines a block by varying the nonce until the hash has targetBits 0s in
// the beginning.  Could take forever if targetBits is too high.
// Modifies a block in place by using a pointer receiver.
func (self *Block) ValidMine(targetBits int) bool {
	// your mining code here
	// also feel free to get rid of this method entirely if you want to
	// organize things a different way; this is just a suggestion
	totalCount := 0
	for i := 0; i < 32; i++ {
		currentByte := self.Hash()[i]
		for j := 128; j >= 1; j = j / 2 {
			if int(currentByte)&j != 0 {
				return false
			}
			totalCount += 1
			if totalCount >= targetBits {
				return true
			}
		}
	}
	return false
}
