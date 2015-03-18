#include <stdio.h>
#include <stdlib.h>
#include <malloc.h>
#include <sys/mman.h>

char * malloc_and_mlock(size_t size)
{
	char * buffer;
	unsigned long i;
	buffer = (char *) valloc (size);
	if (buffer != 0)
	{
		mlockall(MCL_CURRENT);
		for (i=0;i<size;i++)
		{
			buffer[i] = 0x1e;
		}
	}
	return buffer;
}
