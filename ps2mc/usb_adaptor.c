#include <stdio.h>
#include <errno.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

#include "psx.h"
#include "ps1.h"
#include "ps2.h"

int write_cmd(usb_dev_handle *udev, unsigned char *cmd, int read);

/*
 * unsigned char mycmd[][] = {
	{0x81
	{0xaa, 0x42, 0x04, 0x00, 0x81, 0x11,
*/
int main(void)
{
	usb_dev_handle *udev = NULL;
	unsigned char *string;
	unsigned char data_t[8192];
	int ret, i;

	udev = find_mcrw();

	if (udev)
	{
		init_mcrw(udev);
		/* open device for transfer */
		open_mcrw(udev);

		/* send/receive data */
		//mc1rw_read_page(udev, 0);
		for (i=0; i<8192; i++)
			data_t[i] = 0x00;
		mc1rw_write_block(udev, 14, data_t); 
		//mc1rw_read_page(udev, 0);
		
		/* when we're done close device */
		close_mcrw(udev);
		cleanup_mcrw(udev);
		usb_close(udev);
	}
	printf("DONE!\n");
	return 0;
}

int write_cmd(usb_dev_handle *udev, unsigned char *cmd, int read)
{
	int ret=0, i=0;

	unsigned char receive_data[1024];
	for (i=0; i<1024; i++)
		receive_data[i] = 0x00;

	printf("write_cmd\n");
	ret = usb_bulk_write(udev, 0x02, cmd, sizeof(cmd), 10000);
	if (ret != sizeof(cmd))
		printf("Error!\n");
	
	ret = usb_bulk_read(udev, 0x81, receive_data, sizeof(receive_data), 10000);
	mcrw_debug(receive_data, ret);
	return 0;
}


