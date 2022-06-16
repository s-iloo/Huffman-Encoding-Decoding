from ordered_list import OrderedList
from huffman_bit_writer import HuffmanBitWriter
from huffman_bit_reader import HuffmanBitReader

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char   # stored as an integer - the ASCII character code value
        self.freq = freq   # the freqency associated with the node
        self.left = None   # Huffman tree (node) to the left
        self.right = None  # Huffman tree (node) to the right
        
    def __eq__(self, other):
        '''Needed in order to be inserted into OrderedList''' 
        if other == None:
            return False
        if self.freq == other.freq:
           return self.char == other.char     
        return self.freq == other.freq

    def __lt__(self, other):
        '''Needed in order to be inserted into OrderedList'''
        #returns true if self should come before orther
        #print("whadaa")
        if other == None:
            return False
        if self.freq == other.freq:
            return self.char < other.char
        return self.freq < other.freq
    
def cnt_freq(filename):
    '''Opens a text file with a given file name (passed as a string) and counts the 
    frequency of occurrences of all the characters within that file'''
    file = open(filename, "r")
    content = file.read()
    myList = [0]*256
    for j in content:
        myIndex = ord(j) #set equal to the ascii value
        myList[myIndex] = myList[myIndex] + 1
    file.close()
    return myList
    #check all the content of the string and then make a list with the ascii values

def create_huff_tree(char_freq):
    '''Create a Huffman tree for characters with non-zero frequency
    Returns the root node of the Huffman tree'''
    #gets the list and creates the huffman tree
    orderedList = OrderedList()
    #empty and one char??

    for i in range(256):
        if char_freq[i] != 0:
            huffNode = HuffmanNode(i, char_freq[i])
            orderedList.add(huffNode)
    
    if orderedList.size() == 0:
        return None

    if orderedList.size() == 1:
        myNode = orderedList.pop(0)
        newHuff = HuffmanNode(myNode.char, myNode.freq)
        return newHuff
        #pop the two nodes with lowest freq count and connect to left and right
        #of new created huffman node 
    while orderedList.size() > 1:
        #pop the two lowest frequencies
        first = orderedList.pop(0)
        second = orderedList.pop(0)
        newAsc = min(first.char, second.char)
        newHuff = HuffmanNode(newAsc, first.freq + second.freq)
        newHuff.left = first
        newHuff.right = second
        orderedList.add(newHuff)
    
    return newHuff

def create_code(node):
    '''Returns an array (Python list) of Huffman codes. For each character, use the integer ASCII representation 
    as the index into the arrary, with the resulting Huffman code for that character stored at that location'''
    a = [''] * 256
    create_code_helper(node, a, '')
    return a

def create_code_helper(node, a, myStr):
    #base case when place is none
    #what if its empty and one char

    if node.left == None and node.right == None:

        a[node.char] = myStr
        myStr = ''
        #need to move back to the root and keep going
    #traverse down the left subtree
    if node.left != None:
        create_code_helper(node.left, a, myStr + "0")
    if node.right != None:
        create_code_helper(node.right, a, myStr + "1")
def create_header(freqs):
    '''Input is the list of frequencies. Creates and returns a header for the output file
    Example: For the frequency list asscoaied with "aaabbbbcc, would return “97 3 98 4 99 2” '''
    returned = ''
    for i in range(len(freqs)):
        if freqs[i] != 0:
            ascii = str(i)
            freq = str(freqs[i])
            returned += ascii + " " + freq + " " 
    return returned[:-1] 

def huffman_encode(in_file, out_file):
    '''Takes inout file name and output file name as parameters - both files will have .txt extensions
    Uses the Huffman coding process on the text from the input file and writes encoded text to output file
    Also creates a second output file which adds _compressed before the .txt extension to the name of the file.
    This second file is actually compressed by writing individual 0 and 1 bits to the file using the utility methods 
    provided in the huffman_bits_io module to write both the header and bits.
    Take not of special cases - empty file and file with only one unique character'''
    
    #needs to return two files one compressed and one uncompressed(text file)
    try:
        file = open(in_file, "r")
        file.close()
    except FileNotFoundError:
        raise FileNotFoundError
    #check if the file is empty

    r = open(in_file, "r")
    maybeEmpty = r.read()
    r.close()
    if maybeEmpty == "":
        compressedFile = out_file[:len(out_file) - 4] + "_compressed" + out_file[len(out_file) - 4:]
        o = open(compressedFile, "w")
        o.close()

        out = open(out_file, "w")
        out.close()

        return out_file, compressedFile

    i = open(in_file, "r")
    o = open(out_file, "w")

    header = create_header(cnt_freq(in_file))
    freq = cnt_freq(in_file)
    huffTree = create_huff_tree(freq)
    encodedTxt = create_code(huffTree)
    myStr = ''

    read = i.read()
    i.close()

    for i in read:
        myStr += encodedTxt[ord(i)]
    
    o.write(header + "\n" + myStr)
    o.close()

    newOutputName = out_file[:len(out_file) - 4] + "_compressed" + out_file[len(out_file) - 4:]
    bitWriter = HuffmanBitWriter(newOutputName)
    bitWriter.write_str(header + "\n")
    bitWriter.write_code(myStr)
    bitWriter.close()

    return newOutputName, out_file


def parse_header(header_string):
    header = header_string.split()
    freqs = [0] * 256
    ascii = 0
    #freq = 1


    for i in range(len(header)//2):
        if ascii < len(header):
            freqs[int(header[ascii])] = int(header[ascii + 1])
            ascii += 2

    return freqs



def huffman_decode(encoded_file, decode_file):
    #reads the encoded text file and writes the decoded text into an output text file
    #using the huffman tree produced by using the header information
    #if encoded file dne raise FileNotFoundError 
    #if specified output file already exists its old contents will be overwritten
    
    #before recreating huff tree create list_of_freqs from the info stored in the header
    #use the huffman bit reader class to read the header

    try:
        f = open(encoded_file, "r")
        f.close()
    except:
        raise FileNotFoundError

    e = open(encoded_file, "r")
    d = open(decode_file, "w")
    reader = HuffmanBitReader(encoded_file)
    content = reader.read_str()
    header = parse_header(content)
    myHuffTree = create_huff_tree(header) #returns the root node of the hufftree
    numWords = 0
    totalFreqs = 0
    #need to read the bits now using bit reader
    for i in header:
        if i != 0:
            totalFreqs += i 

    while totalFreqs != numWords:
        next = myHuffTree
        while next.left != None and next.right != None:
            oneorzero = reader.read_bit()
            if oneorzero == False:
                next = next.left
                #print("0")
            else:
                next = next.right
                #print("1")
        myChar = next.char
        d.write(chr(myChar))

        numWords += 1
    reader.close()
    e.close()
    d.close()


#myInput = huffman_encode("file1.txt", "file1out.txt")


#huffman_decode("file1_compressed_soln.txt", "file1decode.txt")