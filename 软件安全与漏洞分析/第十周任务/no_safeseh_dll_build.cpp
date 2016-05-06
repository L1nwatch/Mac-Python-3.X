#include <WINDOWS.H>
BOOL APIENTRY DllMain( HANDLE hModule,DWORD  ul_reason_for_call, LPVOID lpReserved) {
    return TRUE;
}
void jump() {
	__asm{
		pop eax
		pop eax
		retn
	}
}