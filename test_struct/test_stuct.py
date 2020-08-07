import struct

# with open('etc.zip', 'rb') as f:
#     data = f.read()

# start = 0
# for i in range(3):                      # show the first 3 file headers
#     start += 14
#     fields = struct.unpack('<IIIHH', data[start:start+16])
#     crc32, comp_size, uncomp_size, filenamesize, extra_size = fields

#     start += 16
#     filename = data[start:start+filenamesize]
#     start += filenamesize
#     extra = data[start:start+extra_size]
#     print(filename, hex(crc32), comp_size, uncomp_size)

#     start += extra_size + comp_size     # skip to the next header

def parse_chunk_table(file_name):
    with open(file_name, 'rb') as f:
        data = f.read()

    start = 0
    #[list $magic_number $table_version $align_head $parse_config $base_offset $base2_offset $table_size [expr $num_chunks + 1] $sec_attr $sec_key_num $sec_key1 $sec_key2 $sec_key3 $sec_key4]
    header_len = 4*14
    fields = struct.unpack('<14I', data[start:start+header_len])
    magic_number, table_version, align_head, parse_config ,base_offset ,base2_offset ,table_size, num_chunks ,sec_attr ,sec_key_num ,sec_key1 ,sec_key2 ,sec_key3 ,sec_key4 = fields
    print('='*160)
    headr_fmt =  '{{:^{}}}'.format(15)
    headrs_fmt = headr_fmt*14
    print(headrs_fmt.format('magic_number', 'table_version', 'align_head', 'parse_config' ,'base_offset' ,'base2_offset' ,'table_size', 'num_chunks' ,'sec_attr' ,'sec_key_num' ,'sec_key1' ,'sec_key2' ,'sec_key3' ,'sec_key4' ))
    print(headrs_fmt.format(hex(magic_number), table_version, align_head, parse_config ,base_offset ,base2_offset ,table_size, num_chunks ,sec_attr ,sec_key_num ,sec_key1 ,sec_key2 ,sec_key3 ,sec_key4))
    print('='*160)
    start = start+header_len
    item_fmt =  '{{:^{}}}'.format(15)
    items_fmt = item_fmt*8
    print(items_fmt.format('chunk_codetype', 'chunk_offset', 'chunk_size', 'chunk_dest', 'chunk_length', 'chunk_type', 'chunk_attr', 'res2'))
    for i in range(num_chunks): 
        #$chunk_codetype $chunk_offset $chunk_size $chunk_dest $chunk_length $chunk_type $chunk_attr $res2
        fields = struct.unpack('<8I', data[start:start+32])
        chunk_codetype, chunk_offset, chunk_size, chunk_dest, chunk_length, chunk_type, chunk_attr, res2 = fields

        start += 32
        print(items_fmt.format(chunk_codetype, chunk_offset, chunk_size, hex(chunk_dest), chunk_length, chunk_type, chunk_attr, res2))
    print('='*160)

def main():
    parse_chunk_table("chunk_table.binary")


if __name__ == '__main__':
    main()