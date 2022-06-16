import unittest
import filecmp
import subprocess
from ordered_list import *
from huffman import *


class TestList(unittest.TestCase):
    def test_cnt_freq(self):
        freqlist	= cnt_freq("file2.txt")
        anslist = [2, 4, 8, 16, 0, 2, 0] 
        self.assertListEqual(freqlist[97:104], anslist)

    #need to test what happens if you try to assert equal or assert less than for other types 

    def testotherequalnone(self):
        self.assertFalse(HuffmanNode(20, 15) == None)
    def testotherlessthannone(self):
        self.assertFalse(HuffmanNode(20, 15) < None)

    def test_lt_and_eq(self):
        freqlist	= cnt_freq("file2.txt")
        anslist = [2, 4, 8, 16, 0, 2, 0] 
        #  ordered list should be -> [0, 0, 2, 2, 4, 8, 16]
        #  what happens -> []
        
        ascii = 97
        lst = OrderedList()

        for freq in anslist:
            node = HuffmanNode(ascii, freq)
            lst.add(node)
            ascii += 1

        self.assertEqual(lst.index(HuffmanNode(97, 2)), 2)
        self.assertEqual(lst.index(HuffmanNode(100, 16)), 6)
        self.assertEqual(lst.index(HuffmanNode(101, 0)), 0)
        self.assertEqual(lst.index(HuffmanNode(102, 2)), 3)
        self.assertFalse(HuffmanNode(97, 2) == None)
    
    def testltagain(self):
        l = OrderedList()
        l.add(HuffmanNode(32, 3))
        l.add(HuffmanNode(98, 3))
        self.assertEqual(l.index(HuffmanNode(32, 3)), 0)
        self.assertEqual(l.index(HuffmanNode(98, 3)), 1)
        self.assertEqual(HuffmanNode(20, 3) == None, False)
                    
    def test_create_huff_tree(self):
        freqlist = cnt_freq("file2.txt")
        hufftree = create_huff_tree(freqlist)
        self.assertEqual(hufftree.freq, 32)
        self.assertEqual(hufftree.char, 97)
        left = hufftree.left
        self.assertEqual(left.freq, 16)
        self.assertEqual(left.char, 97)
        right = hufftree.right
        self.assertEqual(right.freq, 16)
        self.assertEqual(right.char, 100)

        
    def test_create_header(self):
        freqlist = cnt_freq("file2.txt")
        self.assertEqual(create_header(freqlist), "97 2 98 4 99 8 100 16 102 2")

        
    def test_create_code(self):
        freqlist = cnt_freq("file2.txt")
        hufftree = create_huff_tree(freqlist)
        codes = create_code(hufftree)
        self.assertEqual(codes[ord('d')], '1')
        self.assertEqual(codes[ord('a')], '0000')
        self.assertEqual(codes[ord('f')], '0001')

    def test_emptyheader(self):
        freqlist = cnt_freq("empty_file.txt")
        self.assertEqual(create_header(freqlist), "")
        self.assertEqual(create_huff_tree(freqlist), None)

    #edge case
    def testmultiline(self):
        huffman_encode("multiline.txt", "multilineout.txt")
        err = subprocess.call("diff -wb multilineout.txt multiline_soln.txt", shell = True)
        self.assertEqual(err, 0)
        err = subprocess.call("diff -wb multilineout_compressed.txt multiline_compressed_soln.txt", shell = True)
        self.assertEqual(err, 0)
        huffman_encode("declaration.txt", "declarationout.txt")
        err = subprocess.call("diff -wb declarationout.txt declaration_soln.txt", shell = True)
        self.assertEqual(err, 0)
        err = subprocess.call("diff -wb declarationout_compressed.txt declaration_compressed_soln.txt", shell = True)

    def test_01_textfile(self):
        huffman_encode("file1.txt", "file1_out.txt")
        # capture errors by running 'diff' on your encoded file with a *known* solution file
        err = subprocess.call("diff -wb file1_out.txt file1_soln.txt", shell = True)
        self.assertEqual(err, 0)
        err = subprocess.call("diff -wb file1_out_compressed.txt file1_compressed_soln.txt", shell = True)
        self.assertEqual(err, 0)
    #test an empty file which is supposed to return two empty files

    def test2textfile(self):
        huffman_encode("empty_file.txt", "empty_fileout.txt")
        err = subprocess.call("diff -wb empty_fileout.txt emptyfilesoln.txt", shell = True)
        self.assertEqual(err, 0)
        err = subprocess.call("diff -wb empty_fileout_compressed.txt emptyfilesoln.txt", shell = True)
        self.assertEqual(err, 0)

    def testeqwithtypeerrors(self):
        self.assertEqual(HuffmanNode("a", 120) == HuffmanNode(120, "a"), False)

    def testltwithtypeerrors(self):
        with self.assertRaises(FileNotFoundError):
            huffman_encode("heyoyoyo.txt", "nice.txt")

    #for the create huff tree 63-65
    def testoneHuffNode(self): 
        huffman_encode("uniqchar.txt", "uniqcharout.txt")
        err = subprocess.call("diff -wb uniqcharout.txt uniqcharsoln.txt", shell = True)
        self.assertEqual(err, 0)
        err = subprocess.call("diff -wb uniqcharout_compressed.txt uniqchar_compressed.txt", shell = True)
        self.assertEqual(err, 0)

    def testparseheader(self):
        freqs = cnt_freq("file1.txt")
        header = create_header(freqs)
        parse = parse_header(header)
        self.assertEqual(parse, freqs)

    def testnofile(self):
        with self.assertRaises(FileNotFoundError):
            huffman_decode("heyoyoyo.txt", "nice.txt")
    
    def testfile1decode(self):
        huffman_decode("file1_compressed_soln.txt" , "file1decode.txt")
        decode = open("file1decode.txt", "r")
        decoderead = decode.read()
        decode.close()
        og = open("file1.txt", "r")
        ogread = og.read()
        og.close()
        self.assertEqual(ogread, decoderead)
        
        


if __name__ == '__main__': 
   unittest.main()
