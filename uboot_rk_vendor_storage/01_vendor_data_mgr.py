#!/usr/bin/env python
"""
This script can read, and (partially) modify, the vendor data block used in the
rockchip u-boot. The implementation follows information gathered from the
rockchip u-boot, which is licensed under the GPL-2.0+ license.

Used file from the u-boot code: arch/arm/mach-rockchip/vendor.c

e.g., found here:

https://github.com/m-weigand/u-boot-pinenote/blob/branch_cyttsp5ub/arch/arm/mach-rockchip/vendor.c

# License for u-boot:


 (C) Copyright 2000 - 2013
 Wolfgang Denk, DENX Software Engineering, wd@denx.de.

 SPDX-License-Identifier:      GPL-2.0+

# License/copyright in vendor.c:

 (C) Copyright 2008-2017 Fuzhou Rockchip Electronics Co., Ltd

 SPDX-License-Identifier: GPL-2.0+

"""
import os
import shutil
import struct


class vendor_data(object):
    def __init__(self, filename=None, vendor_img=None):
        # each data block starts with this u32 value
        self.vendor_tag = 0x524B5644
        '''
         60 struct vendor_hdr {
         61     u32 tag;
         62     u32 version;
         63     u16 next_index;
         64     u16 item_num;
         65     u16 free_offset; /* Free space offset */
         66     u16 free_size; /* Free space size */
         67 };
         vendor_hdr_size_bytes = 16
         14 struct vendor_item {
         15     u16  id;
         16     u16  offset;
         17     u16  size;
         18     u16  flag;
         19 };
         '''
        self.vendor_hdr_size_bytes = 16
        self.vendor_item_size_bytes = 8
        # hardcode the emmc offsets here
        # size of each of the four vendor info blocks = 64 kb
        self.emmc_vendor_info_size = 128 * 512
        self.emmc_version2_offset = self.emmc_vendor_info_size - 4
        # MMC DATA OFFSET
        self.data_offset = 1024

        self.filename = filename
        self.vendor_img = vendor_img
        self.blocks = []

        self.read_data()

    def read_data(self):
        if self.filename is not None:
            with open(self.filename, 'rb') as fid:
                print('Reading vendor data from full disc image')
                fid.seek(7168 * 512)
                block1 = fid.read(128 * 512)
                block2 = fid.read(128 * 512)
                block3 = fid.read(128 * 512)
                block4 = fid.read(128 * 512)

                self.blocks += [
                    block1,
                    block2,
                    block3,
                    block4,
                ]
        elif self.vendor_img is not None:
            print('Opening vendor data block')
            with open(self.vendor_img, 'rb') as fid:
                block1 = fid.read(128 * 512)
                block2 = fid.read(128 * 512)
                block3 = fid.read(128 * 512)
                block4 = fid.read(128 * 512)

                self.blocks += [
                    block1,
                    block2,
                    block3,
                    block4,
                ]

        else:
            raise Exception(
                'You need to provide either a filename starting ' +
                'from byte 0, or a vendor image file with 256 kb'
            )

    def _get_hdr(self, block):
        """Get the header (hdr) from a block of bytes"""
        values = struct.unpack('IIHHHH', block[0: self.vendor_hdr_size_bytes])
        hdr = {}
        hdr['tag'] = values[0]
        hdr['version'] = values[1]
        hdr['next_index'] = values[2]
        hdr['item_num'] = values[3]
        hdr['free_offset'] = values[4]
        hdr['free_size'] = values[5]
        return hdr

    def _set_hdr(self, blockl, hdr_new):
        assert isinstance(blockl, list)
        data = struct.pack(
            'IIHHHH',
            hdr_new['tag'],
            hdr_new['version'],
            hdr_new['next_index'],
            hdr_new['item_num'],
            hdr_new['free_offset'],
            hdr_new['free_size'],
        )
        blockl[0:self.vendor_hdr_size_bytes] = data

    def _get_version2(self, block):
        version2 = struct.unpack('I', block[-4:])[0]
        return version2

    def _set_version2(self, blockl, new_version2):
        version2_new = struct.pack('I', new_version2)
        blockl[-4:] = version2_new

    def _get_item_info(self, block):
        hdr = self._get_hdr(block)
        # print(hdr)
        items = []
        for item_index in range(0, hdr['item_num']):
            start = self.vendor_hdr_size_bytes + \
                item_index * self.vendor_item_size_bytes

            values = struct.unpack(
                'HHHH',
                block[start: start + self.vendor_item_size_bytes]
            )
            item = {
                'id': values[0],
                'offset': values[1],
                'size': values[2],
                'flag': values[3],
            }
            items += [item]
        return items

    def _set_item(self, blockl, item_index, new_item):
        data_new = struct.pack(
            'HHHH',
            new_item['id'],
            new_item['offset'],
            new_item['size'],
            new_item['flag'],
        )
        start = self.vendor_hdr_size_bytes + \
            item_index * self.vendor_item_size_bytes
        blockl[start:start+self.vendor_item_size_bytes] = data_new

    def get_newest_block_id(self):
        hversion = -1
        hindex = -1

        for index, block in enumerate(self.blocks):
            hdr = self._get_hdr(block)
            if hdr['version'] > hversion:
                # found a newer block
                hversion = hdr['version']
                hindex = index
        print('Newest block is:', hindex, ' with version', hversion)
        return hindex

    def get_item_data(self, block, item_id):
        items = self._get_item_info(block)
        for item in items:
            if item['id'] == item_id:
                start = self.data_offset + item['offset']
                end = start + item['size']
                data = block[start:end]
                return data
        return None

    def print_vendor_info(self):
        self.get_newest_block_id()
        for nr, block in enumerate(self.blocks):
            print('----- BLOCK NR: {} -----'.format(nr))
            # print(vendor._get_hdr(block))
            print('version2:', vendor._get_version2(block))
            items = vendor._get_item_info(block)
            print(items)
            print('DATA:')
            for item in items:
                data = self.get_item_data(block, item['id'])
                print(' ' * 4, item['id'], ':', data)
            print('')
            print('')
            print('')

    def update_item(self, item_id, new_data):
        '''
        1) find newest block
        2) copy block to next_index
        3) work on next index block:
            3a) adjust next_index
            3b) write new data
            3c) update version
            3d) update version2
        '''
        hindex = self.get_newest_block_id()
        block = self.blocks[hindex]
        hdr = self._get_hdr(block)
        items = self._get_item_info(block)

        print(hdr['next_index'])
        blockl = list(block)
        hdr_new = hdr.copy()
        hdr_new['version'] += 1
        hdr_new['next_index'] = (hdr_new['next_index'] + 1) % 4
        self._set_hdr(blockl, hdr_new)
        self._set_version2(blockl, hdr_new['version'])

        # find item that we want to change
        target_item = None
        target_item_index = None
        for item_index, item in enumerate(items):
            if item['id'] == item_id:
                target_item = item
                target_item_index = item_index
        assert target_item is not None

        # change data
        start = self.data_offset + target_item['offset']
        data_new = bytearray(len(new_data) + 1)
        data_new_length = len(data_new)
        print('new length', data_new_length)
        data_new[0:-1] = bytes(new_data, 'ascii')
        blockl[start:start + data_new_length] = data_new

        target_item['size'] = data_new_length
        self._set_item(blockl, target_item_index, target_item)
        # import IPython
        # IPython.embed()

        # replace old block at index 'next_index' with new one
        self.blocks[hdr['next_index']] = bytes(blockl)

    def write_to_vendor_info_to_file_copy(self, filename):
        """Given a binary blob starting at block zero of the PN disc,
        copy the file and overwrite the vendor block with the one stored in
        this class.

        Parameters
        ----------

        filename : str
            Output filename. Must not be the same as the input filename

        """
        assert self.filename != filename
        assert not os.path.isfile(filename), 'Output file must not exist'

        shutil.copy(self.filename, filename)
        with open(filename, 'r+b') as fid:
            for index, block in enumerate(self.blocks):
                fid.seek(7168 * 512 + index * 128 * 512)
                fid.write(block)

    def write_new_vendor_block(self, filename):
        assert self.filename != filename
        assert not os.path.isfile(filename), 'Output file must not exist'

        with open(filename, 'wb') as fid:
            for index, block in enumerate(self.blocks):
                fid.write(block)


if __name__ == '__main__':
    # Variant 1: Read the vendor data from a disc dump (i.e., seek the location
    # of the vendor data block within the file)
    if False:
        # vendor = vendor_data('first8MB.bin')
        vendor = vendor_data('test.bin')
        vendor.print_vendor_info()

        print('UPDATING')
        vendor.update_item(17, '930')
        print('DONE')
        vendor.print_vendor_info()

        # print('Writing to new file')
        # vendor.write_to_vendor_info_to_file_copy('output.bin')
        # vendor1 = vendor_data('output.bin')
        # vendor1.print_vendor_info()

    # variant 2: work only on the actual vendor data
    if True:
        vendor = vendor_data(vendor_img='vendor.bin')
        vendor.print_vendor_info()
        vendor.update_item(17, '930')
        vendor.print_vendor_info()
        # vendor.write_new_vendor_block('vendor_fixed.bin')
