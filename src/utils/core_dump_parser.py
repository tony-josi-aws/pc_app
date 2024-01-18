import sys
import datetime

class core_dump_parser:
    def __init( self ):
        # Exception info
        self.uxFileExistMagic = 0
        self.uxTotalLength = 0
        self.uxRegDumpOffset = 0
        self.uxRegDumpLength = 0
        self.uxMemoryRegionNum = 0

        self.data_offset = 0
        self.data_length = 0
        self.data_address = 0
        self.dataBankMemory = []

        self.bss_offset = 0
        self.bss_length = 0
        self.bss_address = 0
        self.bssBankMemory = []

        self.uxFileEndMagic = 0

        # Core register
        self.ulRegR0 = 0
        self.ulRegR1 = 0
        self.ulRegR2 = 0
        self.ulRegR3 = 0
        self.ulRegR4 = 0
        self.ulRegR5 = 0
        self.ulRegR6 = 0
        self.ulRegR7 = 0
        self.ulRegR8 = 0
        self.ulRegR9 = 0
        self.ulRegR10 = 0
        self.ulRegR11 = 0
        self.ulRegR12 = 0
        self.ulRegSp = 0
        self.ulRegLr = 0
        self.ulRegPc = 0
        self.ulRegXpsr = 0
        self.ulRegD0 = 0
        self.ulRegD1 = 0
        self.ulRegD2 = 0
        self.ulRegD3 = 0
        self.ulRegD4 = 0
        self.ulRegD5 = 0
        self.ulRegD6 = 0
        self.ulRegD7 = 0
        self.ulRegD8 = 0
        self.ulRegD9 = 0
        self.ulRegD10 = 0
        self.ulRegD11 = 0
        self.ulRegD12 = 0
        self.ulRegD13 = 0
        self.ulRegD14 = 0
        self.ulRegD15 = 0
        self.ulRegFpscr = 0
        self.ulRegPrimask = 0
        self.ulRegBasepri = 0
        self.ulRegFaultmask = 0
        self.ulRegControl = 0
        self.ulRegMsp = 0
        self.ulRegPsp = 0

    def parse_core_dump( self, FileName, output_file ):
        self.timestamp = int(datetime.datetime.timestamp( datetime.datetime.now() ))

        with open( FileName, 'rb') as reader:
            # Exception information
            self.uxFileExistMagic = int.from_bytes(reader.read(4), byteorder='little')
            self.uxTotalLength = int.from_bytes(reader.read(4), byteorder='little')
            self.uxRegDumpOffset = int.from_bytes(reader.read(4), byteorder='little')
            self.uxRegDumpLength = int.from_bytes(reader.read(4), byteorder='little')

            self.uxMemoryRegionNum = int.from_bytes(reader.read(4), byteorder='little')

            self.data_offset = int.from_bytes(reader.read(4), byteorder='little')
            self.data_length = int.from_bytes(reader.read(4), byteorder='little')
            self.data_address = int.from_bytes(reader.read(4), byteorder='little')

            self.bss_offset = int.from_bytes(reader.read(4), byteorder='little')
            self.bss_length = int.from_bytes(reader.read(4), byteorder='little')
            self.bss_address = int.from_bytes(reader.read(4), byteorder='little')

            # Core Registers
            reader.seek( self.uxRegDumpOffset )
            self.ulRegR0 = int.from_bytes(reader.read(4), byteorder='little')
            self.ulRegR1 = int.from_bytes(reader.read(4), byteorder='little')
            self.ulRegR2 = int.from_bytes(reader.read(4), byteorder='little')
            self.ulRegR3 = int.from_bytes(reader.read(4), byteorder='little')
            self.ulRegR4 = int.from_bytes(reader.read(4), byteorder='little')
            self.ulRegR5 = int.from_bytes(reader.read(4), byteorder='little')
            self.ulRegR6 = int.from_bytes(reader.read(4), byteorder='little')
            self.ulRegR7 = int.from_bytes(reader.read(4), byteorder='little')
            self.ulRegR8 = int.from_bytes(reader.read(4), byteorder='little')
            self.ulRegR9 = int.from_bytes(reader.read(4), byteorder='little')
            self.ulRegR10 = int.from_bytes(reader.read(4), byteorder='little')
            self.ulRegR11 = int.from_bytes(reader.read(4), byteorder='little')
            self.ulRegR12 = int.from_bytes(reader.read(4), byteorder='little')
            self.ulRegSp = int.from_bytes(reader.read(4), byteorder='little')
            self.ulRegLr = int.from_bytes(reader.read(4), byteorder='little')
            self.ulRegPc = int.from_bytes(reader.read(4), byteorder='little')
            self.ulRegXpsr = int.from_bytes(reader.read(4), byteorder='little')
            self.ulRegD0 = int.from_bytes(reader.read(4), byteorder='little')
            self.ulRegD1 = int.from_bytes(reader.read(4), byteorder='little')
            self.ulRegD2 = int.from_bytes(reader.read(4), byteorder='little')
            self.ulRegD3 = int.from_bytes(reader.read(4), byteorder='little')
            self.ulRegD4 = int.from_bytes(reader.read(4), byteorder='little')
            self.ulRegD5 = int.from_bytes(reader.read(4), byteorder='little')
            self.ulRegD6 = int.from_bytes(reader.read(4), byteorder='little')
            self.ulRegD7 = int.from_bytes(reader.read(4), byteorder='little')
            self.ulRegD8 = int.from_bytes(reader.read(4), byteorder='little')
            self.ulRegD9 = int.from_bytes(reader.read(4), byteorder='little')
            self.ulRegD10 = int.from_bytes(reader.read(4), byteorder='little')
            self.ulRegD11 = int.from_bytes(reader.read(4), byteorder='little')
            self.ulRegD12 = int.from_bytes(reader.read(4), byteorder='little')
            self.ulRegD13 = int.from_bytes(reader.read(4), byteorder='little')
            self.ulRegD14 = int.from_bytes(reader.read(4), byteorder='little')
            self.ulRegD15 = int.from_bytes(reader.read(4), byteorder='little')
            self.ulRegFpscr = int.from_bytes(reader.read(4), byteorder='little')
            self.ulRegPrimask = int.from_bytes(reader.read(4), byteorder='little')
            self.ulRegBasepri = int.from_bytes(reader.read(4), byteorder='little')
            self.ulRegFaultmask = int.from_bytes(reader.read(4), byteorder='little')
            self.ulRegControl = int.from_bytes(reader.read(4), byteorder='little')
            self.ulRegMsp = int.from_bytes(reader.read(4), byteorder='little')
            self.ulRegPsp = int.from_bytes(reader.read(4), byteorder='little')

            # .data section
            reader.seek( self.data_offset )
            self.dataBankMemory = []
            for i in range( int( self.data_length / 4 ) ):
                self.dataBankMemory.append( int.from_bytes(reader.read(4), byteorder='little') )

            # .bss section
            reader.seek( self.bss_offset )
            self.bssBankMemory = []
            for i in range( int(self.bss_length / 4) ):
                self.bssBankMemory.append( int.from_bytes(reader.read(4), byteorder='little') )

            # end magic
            reader.seek( self.uxTotalLength - 4 )
            self.uxFileEndMagic = int.from_bytes(reader.read(4), byteorder='little')

            # print( hex( self.bss_address ) )
            # print( hex( self.bss_length ) )
            # print( hex( self.bss_offset ) )

            # print( hex( self.data_address ) )
            # print( hex( self.data_length ) )
            # print( hex( self.data_offset ) )

            # print( hex( self.uxFileExistMagic ) )

        return self.dump_gdb_txt_format(output_file)

    def dump_gdb_txt_format( self, output_file ):
        if output_file == None or output_file == "":
            coredump_parsed_file_name = str(hex(random.getrandbits(64)))
            coredump_parsed_file_name = coredump_parsed_file_name[2:]
            coredump_parsed_file_name += ".dump"
            fileName = coredump_parsed_file_name
        else:
            fileName = output_file
        fp = open( fileName , "w")

        currentAddress = self.data_address
        iterateTime = 0
        isFirst = True
        for x in self.dataBankMemory:
            if isFirst != True and (iterateTime % 4) == 0:
                print("", file=fp)
            else:
                isFirst = False

            if (iterateTime % 4) == 0:
                print( "0x{:08x}".format(currentAddress) + ":\t", end="", file=fp )
                currentAddress += 16
            else:
                print( "\t", end="", file=fp )
            print( "0x{:08x}".format(x), end="", file=fp )
            iterateTime = iterateTime + 1
        print("", file=fp)

        currentAddress = self.bss_address
        iterateTime = 0
        isFirst = True
        for x in self.bssBankMemory:
            if isFirst != True and (iterateTime % 4) == 0:
                print("", file=fp)
            else:
                isFirst = False

            if (iterateTime % 4) == 0:
                print( "0x{:08x}".format(currentAddress) + ":\t", end="", file=fp )
                currentAddress += 16
            else:
                print( "\t", end="", file=fp )
            print( "0x{:08x}".format(x), end="", file=fp )
            iterateTime = iterateTime + 1
        print("", file=fp)

        print("r0             " + str(hex(self.ulRegR0)) + "                 " + str(self.ulRegR0), file=fp)
        print("r1             " + str(hex(self.ulRegR1)) + "                 " + str(self.ulRegR1), file=fp)
        print("r2             " + str(hex(self.ulRegR2)) + "                 " + str(self.ulRegR2), file=fp)
        print("r3             " + str(hex(self.ulRegR3)) + "                 " + str(self.ulRegR3), file=fp)
        print("r4             " + str(hex(self.ulRegR4)) + "                 " + str(self.ulRegR4), file=fp)
        print("r5             " + str(hex(self.ulRegR5)) + "                 " + str(self.ulRegR5), file=fp)
        print("r6             " + str(hex(self.ulRegR6)) + "                 " + str(self.ulRegR6), file=fp)
        print("r7             " + str(hex(self.ulRegR7)) + "                 " + str(self.ulRegR7), file=fp)
        print("r8             " + str(hex(self.ulRegR8)) + "                 " + str(self.ulRegR8), file=fp)
        print("r9             " + str(hex(self.ulRegR9)) + "                 " + str(self.ulRegR9), file=fp)
        print("r10            " + str(hex(self.ulRegR10)) + "                 " + str(self.ulRegR10), file=fp)
        print("r11            " + str(hex(self.ulRegR11)) + "                 " + str(self.ulRegR11), file=fp)
        print("r12            " + str(hex(self.ulRegR12)) + "                 " + str(self.ulRegR12), file=fp)
        print("sp             " + str(hex(self.ulRegSp)) + "                 " + str(hex(self.ulRegSp)), file=fp)
        print("lr             " + str(hex(self.ulRegLr)) + "                 " + str(self.ulRegLr), file=fp)
        print("pc             " + str(hex(self.ulRegPc)) + "                 " + str(hex(self.ulRegPc)), file=fp)
        print("xpsr           " + str(hex(self.ulRegXpsr)) + "                 " + str(self.ulRegXpsr), file=fp)
        print("d0             " + str(self.ulRegD0) + "                 " + "(raw " + "0x{:016x}".format(self.ulRegD0) + ")", file=fp)
        print("d1             " + str(self.ulRegD1) + "                 " + "(raw " + "0x{:016x}".format(self.ulRegD1) + ")", file=fp)
        print("d2             " + str(self.ulRegD2) + "                 " + "(raw " + "0x{:016x}".format(self.ulRegD2) + ")", file=fp)
        print("d3             " + str(self.ulRegD3) + "                 " + "(raw " + "0x{:016x}".format(self.ulRegD3) + ")", file=fp)
        print("d4             " + str(self.ulRegD4) + "                 " + "(raw " + "0x{:016x}".format(self.ulRegD4) + ")", file=fp)
        print("d5             " + str(self.ulRegD5) + "                 " + "(raw " + "0x{:016x}".format(self.ulRegD5) + ")", file=fp)
        print("d6             " + str(self.ulRegD6) + "                 " + "(raw " + "0x{:016x}".format(self.ulRegD6) + ")", file=fp)
        print("d7             " + str(self.ulRegD7) + "                 " + "(raw " + "0x{:016x}".format(self.ulRegD7) + ")", file=fp)
        print("d8             " + str(self.ulRegD8) + "                 " + "(raw " + "0x{:016x}".format(self.ulRegD8) + ")", file=fp)
        print("d9             " + str(self.ulRegD9) + "                 " + "(raw " + "0x{:016x}".format(self.ulRegD9) + ")", file=fp)
        print("d10            " + str(self.ulRegD10) + "                 " + "(raw " + "0x{:016x}".format(self.ulRegD10) + ")", file=fp)
        print("d11            " + str(self.ulRegD11) + "                 " + "(raw " + "0x{:016x}".format(self.ulRegD11) + ")", file=fp)
        print("d12            " + str(self.ulRegD12) + "                 " + "(raw " + "0x{:016x}".format(self.ulRegD12) + ")", file=fp)
        print("d13            " + str(self.ulRegD13) + "                 " + "(raw " + "0x{:016x}".format(self.ulRegD13) + ")", file=fp)
        print("d14            " + str(self.ulRegD14) + "                 " + "(raw " + "0x{:016x}".format(self.ulRegD14) + ")", file=fp)
        print("d15            " + str(self.ulRegD15) + "                 " + "(raw " + "0x{:016x}".format(self.ulRegD15) + ")", file=fp)
        print("fpscr          " + str(hex(self.ulRegFpscr)) + "                 " + str(self.ulRegFpscr), file=fp)
        print("primask        " + str(hex(self.ulRegPrimask)) + "                 " + str(self.ulRegPrimask), file=fp)
        print("basepri        " + str(hex(self.ulRegBasepri)) + "                 " + str(self.ulRegBasepri), file=fp)
        print("faultmask      " + str(hex(self.ulRegFaultmask)) + "                 " + str(self.ulRegFaultmask), file=fp)
        print("control        " + str(hex(self.ulRegControl)) + "                 " + str(self.ulRegControl), file=fp)
        print("msp            " + str(hex(self.ulRegMsp)) + "                 " + str(self.ulRegMsp), file=fp)
        print("psp            " + str(hex(self.ulRegPsp)) + "                 " + str(self.ulRegPsp), file=fp)
        print("s0             0                   (raw 0x00000000)", file=fp)
        print("s1             0                   (raw 0x00000000)", file=fp)
        print("s2             0                   (raw 0x00000000)", file=fp)
        print("s3             0                   (raw 0x00000000)", file=fp)
        print("s4             0                   (raw 0x00000000)", file=fp)
        print("s5             0                   (raw 0x00000000)", file=fp)
        print("s6             0                   (raw 0x00000000)", file=fp)
        print("s7             0                   (raw 0x00000000)", file=fp)
        print("s8             0                   (raw 0x00000000)", file=fp)
        print("s9             0                   (raw 0x00000000)", file=fp)
        print("s10            0                   (raw 0x00000000)", file=fp)
        print("s11            0                   (raw 0x00000000)", file=fp)
        print("s12            0                   (raw 0x00000000)", file=fp)
        print("s13            0                   (raw 0x00000000)", file=fp)
        print("s14            0                   (raw 0x00000000)", file=fp)
        print("s15            0                   (raw 0x00000000)", file=fp)
        print("s16            0                   (raw 0x00000000)", file=fp)
        print("s17            0                   (raw 0x00000000)", file=fp)
        print("s18            0                   (raw 0x00000000)", file=fp)
        print("s19            0                   (raw 0x00000000)", file=fp)
        print("s20            0                   (raw 0x00000000)", file=fp)
        print("s21            0                   (raw 0x00000000)", file=fp)
        print("s22            0                   (raw 0x00000000)", file=fp)
        print("s23            0                   (raw 0x00000000)", file=fp)
        print("s24            0                   (raw 0x00000000)", file=fp)
        print("s25            0                   (raw 0x00000000)", file=fp)
        print("s26            0                   (raw 0x00000000)", file=fp)
        print("s27            0                   (raw 0x00000000)", file=fp)
        print("s28            0                   (raw 0x00000000)", file=fp)
        print("s29            0                   (raw 0x00000000)", file=fp)
        print("s30            0                   (raw 0x00000000)", file=fp)
        print("s31            0                   (raw 0x00000000)", file=fp)

        return fileName

    def show_result( self ):
        # Exception information
        if self.uxFileExistMagic == 0xaabbaabb:
            print( "Match magic pattern." )
        else:
            print( "Mismatch magic pattern." )

        if self.uxFileEndMagic == 0xaabbaabb:
            print( "Match end magic pattern." )
        else:
            print( "Mismatch end magic pattern." )

        print("self.uxFileExistMagic: " + hex( self.uxFileExistMagic ) )
        print("self.uxTotalLength: " + hex( self.uxTotalLength ) )

        print("self.uxRegDumpOffset: " + hex( self.uxRegDumpOffset ) )
        print("self.uxRegDumpLength: " + hex( self.uxRegDumpLength ) )

        print("self.uxMemoryRegionNum: " + hex( self.uxMemoryRegionNum ) )

        print("self.data_offset: " + hex( self.data_offset ) )
        print("self.data_length: " + hex( self.data_length ) )
        print("self.data_address: " + hex( self.data_address ) )

        print("self.bss_offset: " + hex( self.bss_offset ) )
        print("self.bss_length: " + hex( self.bss_length ) )
        print("self.bss_address: " + hex( self.bss_address ) )

        print("self.uxFileEndMagic: " + hex( self.uxFileEndMagic ) )

        # core registers
        print("self.ulRegR0: " + hex(self.ulRegR0))
        print("self.ulRegR1: " + hex(self.ulRegR1))
        print("self.ulRegR2: " + hex(self.ulRegR2))
        print("self.ulRegR3: " + hex(self.ulRegR3))
        print("self.ulRegR4: " + hex(self.ulRegR4))
        print("self.ulRegR5: " + hex(self.ulRegR5))
        print("self.ulRegR6: " + hex(self.ulRegR6))
        print("self.ulRegR7: " + hex(self.ulRegR7))
        print("self.ulRegR8: " + hex(self.ulRegR8))
        print("self.ulRegR9: " + hex(self.ulRegR9))
        print("self.ulRegR10: " + hex(self.ulRegR10))
        print("self.ulRegR11: " + hex(self.ulRegR11))
        print("self.ulRegR12: " + hex(self.ulRegR12))
        print("self.ulRegSp: " + hex(self.ulRegSp))
        print("self.ulRegLr: " + hex(self.ulRegLr))
        print("self.ulRegPc: " + hex(self.ulRegPc))
        print("self.ulRegXpsr: " + hex(self.ulRegXpsr))
        print("self.ulRegD0: " + hex(self.ulRegD0))
        print("self.ulRegD1: " + hex(self.ulRegD1))
        print("self.ulRegD2: " + hex(self.ulRegD2))
        print("self.ulRegD3: " + hex(self.ulRegD3))
        print("self.ulRegD4: " + hex(self.ulRegD4))
        print("self.ulRegD5: " + hex(self.ulRegD5))
        print("self.ulRegD6: " + hex(self.ulRegD6))
        print("self.ulRegD7: " + hex(self.ulRegD7))
        print("self.ulRegD8: " + hex(self.ulRegD8))
        print("self.ulRegD9: " + hex(self.ulRegD9))
        print("self.ulRegD10: " + hex(self.ulRegD10))
        print("self.ulRegD11: " + hex(self.ulRegD11))
        print("self.ulRegD12: " + hex(self.ulRegD12))
        print("self.ulRegD13: " + hex(self.ulRegD13))
        print("self.ulRegD14: " + hex(self.ulRegD14))
        print("self.ulRegD15: " + hex(self.ulRegD15))
        print("self.ulRegFpscr: " + hex(self.ulRegFpscr))
        print("self.ulRegPrimask: " + hex(self.ulRegPrimask))
        print("self.ulRegBasepri: " + hex(self.ulRegBasepri))
        print("self.ulRegFaultmask: " + hex(self.ulRegFaultmask))
        print("self.ulRegControl: " + hex(self.ulRegControl))
        print("self.ulRegMsp: " + hex(self.ulRegMsp))
        print("self.ulRegPsp: " + hex(self.ulRegPsp))

        # .data
        '''
        iterateTime = 1
        for x in self.dataBankMemory:
            print( "iterateTime: " + str(iterateTime) + " hex: ", end="" )
            print( hex(x) )
            iterateTime = iterateTime + 1
        '''

        # .bss
        '''
        iterateTime = 1
        for x in self.dataBankMemory:
            print( "iterateTime: " + str(iterateTime) + " hex: ", end="" )
            print( hex(x) )
            iterateTime = iterateTime + 1
        '''

if __name__ == '__main__':
    coreDumpParser = core_dump_parser()
    coreDumpParser.parse_core_dump( sys.argv[1] )
    coreDumpParser.show_result()