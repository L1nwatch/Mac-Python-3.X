#include <stdio.h>
#include <WINSOCK2.H>
#include <string.h>
#include <stdlib.h>

#pragma comment(lib, "ws2_32.lib")  //加载 ws2_32.dll

#define BUF_SIZE 64

unsigned char shellcode[] = {0x33,0xC0,0x50,0xB8,0x2E,0x65,0x78,0x65,0x50,0xB8,0x63,0x61,0x6C,0x63,0x50,0x8D,0x04,0x24,0x50,0xB9,0xC7,0x93,0xBF,0x77,0xFF,0xD1};

typedef void (*MYPROC)(LPTSTR); 

void client_deal(SOCKET sock, sockaddr_in servAddr,sockaddr fromAddr, int addrLen){
	char outbuf[BUF_SIZE] = {0};
	char receive_buffer[BUF_SIZE] = {0};
	char buffer[BUF_SIZE] = {0};	// BUF_SIZE = 64
	printf("Input a string: ");
	gets(buffer);
	sendto(sock, buffer, strlen(buffer), 0, (struct sockaddr*)&servAddr, sizeof(servAddr));
	int strLen = recvfrom(sock, receive_buffer, BUF_SIZE, 0, &fromAddr, &addrLen);
    printf("Message form server: %s\n", receive_buffer);

	sprintf(buffer, "Test: %.60s", receive_buffer);
	sprintf(outbuf, buffer);
}

int main(void){
	// 测试 shellcode
	/*
	void (*fun)();
	*(int *)&fun=(int)shellcode;
	fun();
	return 0;
	*/
	
	/*
	int * ret;
	HINSTANCE LibHandle;
	MYPROC ProcAdd;
	char sysbuf[7] = "system";
	char cmdbuf[16] = "calc.exe";
	LibHandle = LoadLibrary("msvcrt.dll");
	ProcAdd = (MYPROC)GetProcAddress(LibHandle,sysbuf); // 0x77bf93c7
	(ProcAdd)(cmdbuf);
	return 0;
	*/

	
	//测试 Done
	// __asm{
	// 	xor eax,eax			// "\0"
	// 	push eax
	// 	mov eax,0x6578652e 	// "exe." <- ".exe"
	// 	push eax
	// 	mov eax,0x636c6163 	// "clac" <- "calc"
	// 	push eax
	// 	lea eax,[esp]		// 字符串 "calc.exe" 的地址
	// 	push eax
	// 	mov ecx,0x77bf93c7	// system 调用
	// 	call ecx
	// }
	// return 0;
	

	

    //初始化DLL
    WSADATA wsaData;
    WSAStartup(MAKEWORD(2, 2), &wsaData);
	
    //创建套接字
    SOCKET sock = socket(PF_INET, SOCK_DGRAM, 0);
	
    //服务器地址信息
    sockaddr_in servAddr;
    memset(&servAddr, 0, sizeof(servAddr));  //每个字节都用0填充
    servAddr.sin_family = PF_INET;
    servAddr.sin_addr.s_addr = inet_addr("192.168.117.1");
    servAddr.sin_port = htons(9999);
	
    //不断获取用户输入并发送给服务器，然后接受服务器数据
    sockaddr fromAddr;
    int addrLen = sizeof(fromAddr);
    while(1){
		client_deal(sock, servAddr, fromAddr, addrLen);
    }
	
    closesocket(sock);
    WSACleanup();
    return 0;
}