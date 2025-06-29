// Lucky.cpp : Определяет точку входа для приложения.
//

#include "framework.h"
#include "Lucky.h"
#include <cstdlib>
#include <ctime>
#include <random>
#include <string>
#include <vector>

#define MAX_LOADSTRING 100
#define ID_EDIT   101
#define ID_BUTTON 102
#define ID_LABEL_RESULT   103   // ← новый ID для результата

static std::mt19937_64 rng(static_cast<unsigned long>(time(nullptr)));
std::wstring num;

// Ниже — ровно 21 байт, ни больше ни меньше
static const unsigned char enc_flag[21] = {
    0x3C,0x36,0x3B,0x3D,0x21,0x6B,0x34,0x19,
    0x28,0x69,0x1E,0x6B,0x38,0x36,0x69,0x05,
    0x16,0x6E,0x39,0x31,0x27
};
constexpr unsigned char FLAG_KEY = 0x5A;

std::wstring get_flag() {
    std::wstring flag;
    flag.reserve(21);
    for (int i = 0; i < 21; ++i) {
        wchar_t ch = static_cast<wchar_t>(enc_flag[i] ^ FLAG_KEY);
        flag.push_back(ch);
    }
    return flag;
}

// Глобальные переменные:
HINSTANCE hInst;                                // текущий экземпляр
WCHAR szTitle[MAX_LOADSTRING];                  // Текст строки заголовка
WCHAR szWindowClass[MAX_LOADSTRING];            // имя класса главного окна

// Отправить объявления функций, включенных в этот модуль кода:
ATOM                MyRegisterClass(HINSTANCE hInstance);
BOOL                InitInstance(HINSTANCE, int);
LRESULT CALLBACK    WndProc(HWND, UINT, WPARAM, LPARAM);
INT_PTR CALLBACK    About(HWND, UINT, WPARAM, LPARAM);

int APIENTRY wWinMain(_In_ HINSTANCE hInstance,
                     _In_opt_ HINSTANCE hPrevInstance,
                     _In_ LPWSTR    lpCmdLine,
                     _In_ int       nCmdShow)
{
    srand(static_cast<unsigned>(time(nullptr)));  // сеем генератор

    UNREFERENCED_PARAMETER(hPrevInstance);
    UNREFERENCED_PARAMETER(lpCmdLine);

    // TODO: Разместите код здесь.

    // Инициализация глобальных строк
    LoadStringW(hInstance, IDS_APP_TITLE, szTitle, MAX_LOADSTRING);
    LoadStringW(hInstance, IDC_LUCKY, szWindowClass, MAX_LOADSTRING);
    MyRegisterClass(hInstance);

    // Выполнить инициализацию приложения:
    if (!InitInstance (hInstance, nCmdShow))
    {
        return FALSE;
    }

    HACCEL hAccelTable = LoadAccelerators(hInstance, MAKEINTRESOURCE(IDC_LUCKY));

    MSG msg;

    // Цикл основного сообщения:
    while (GetMessage(&msg, nullptr, 0, 0))
    {
        if (!TranslateAccelerator(msg.hwnd, hAccelTable, &msg))
        {
            TranslateMessage(&msg);
            DispatchMessage(&msg);
        }
    }

    return (int) msg.wParam;
}



//
//  ФУНКЦИЯ: MyRegisterClass()
//
//  ЦЕЛЬ: Регистрирует класс окна.
//
ATOM MyRegisterClass(HINSTANCE hInstance)
{
    WNDCLASSEXW wcex;

    wcex.cbSize = sizeof(WNDCLASSEX);

    wcex.style          = CS_HREDRAW | CS_VREDRAW;
    wcex.lpfnWndProc    = WndProc;
    wcex.cbClsExtra     = 0;
    wcex.cbWndExtra     = 0;
    wcex.hInstance      = hInstance;
    wcex.hIcon          = LoadIcon(hInstance, MAKEINTRESOURCE(IDI_LUCKY));
    wcex.hCursor        = LoadCursor(nullptr, IDC_ARROW);
    wcex.hbrBackground  = (HBRUSH)(COLOR_WINDOW+1);
    wcex.lpszMenuName   = nullptr;
    wcex.lpszClassName  = szWindowClass;
    wcex.hIconSm        = LoadIcon(wcex.hInstance, MAKEINTRESOURCE(IDI_SMALL));

    return RegisterClassExW(&wcex);
}

//
//   ФУНКЦИЯ: InitInstance(HINSTANCE, int)
//
//   ЦЕЛЬ: Сохраняет маркер экземпляра и создает главное окно
//
//   КОММЕНТАРИИ:
//
//        В этой функции маркер экземпляра сохраняется в глобальной переменной, а также
//        создается и выводится главное окно программы.
//
BOOL InitInstance(HINSTANCE hInstance, int nCmdShow)
{
   hInst = hInstance; // Сохранить маркер экземпляра в глобальной переменной

   DWORD style = WS_OVERLAPPEDWINDOW
       & ~WS_THICKFRAME      // убираем рамку для ресайза
       & ~WS_MAXIMIZEBOX;    // убираем кнопку «Развернуть»

   const int clientW = 350;
   const int clientH = 100;

   // Вычисляем, сколько добавить для рамок и заголовка:
   RECT rc = { 0, 0, clientW, clientH };
   AdjustWindowRect(&rc,
       WS_OVERLAPPEDWINDOW    // здесь ваш стиль окна
       & ~WS_THICKFRAME      // если вы убрали ресайз
       & ~WS_MAXIMIZEBOX,    // и кнопку «Макс.»
       FALSE                   // если меню не используется
   );

   // Итоговые ширина и высота окна:
   int winW = rc.right - rc.left;
   int winH = rc.bottom - rc.top;

   // Теперь создаём окно с точным client area:
   HWND hWnd = CreateWindowW(
       szWindowClass, szTitle,
       style,
       CW_USEDEFAULT, CW_USEDEFAULT,
       winW, winH,
       nullptr, nullptr, hInstance, nullptr
   );

   if (!hWnd)
   {
      return FALSE;
   }

   ShowWindow(hWnd, nCmdShow);
   UpdateWindow(hWnd);

   return TRUE;
}

//
//  ФУНКЦИЯ: WndProc(HWND, UINT, WPARAM, LPARAM)
//
//  ЦЕЛЬ: Обрабатывает сообщения в главном окне.
//
//  WM_COMMAND  - обработать меню приложения
//  WM_PAINT    - Отрисовка главного окна
//  WM_DESTROY  - отправить сообщение о выходе и вернуться
//
//
LRESULT CALLBACK WndProc(HWND hWnd, UINT message, WPARAM wParam, LPARAM lParam)
{
    switch (message)
    {
    case WM_CREATE:
        // Лейбл
        CreateWindowW(
            L"STATIC",           // класс
            L"You need to get 421675675765457651096587121:",   // текст лейбла
            WS_VISIBLE | WS_CHILD,
            10, 10, 340, 20,     // x, y, ширина, высота
            hWnd,
            nullptr,
            hInst,
            nullptr
        );
        // Лейбл
        CreateWindowW(
            L"STATIC",           // класс
            L"Your number is:",   // текст лейбла
            WS_VISIBLE | WS_CHILD,
            10, 40, 340, 20,     // x, y, ширина, высота
            hWnd,
            reinterpret_cast<HMENU>(ID_LABEL_RESULT),
            hInst,
            nullptr
        );

        // Кнопка
        CreateWindowW(
            L"BUTTON",
            L"Generate",
            WS_VISIBLE | WS_CHILD,
            135, 70, 80, 20,
            hWnd,
            reinterpret_cast<HMENU>(ID_BUTTON),
            hInst,
            nullptr
        );
        break;
    case WM_COMMAND:
    {
        int wmId = LOWORD(wParam);
        if (wmId == ID_BUTTON) {
            // Распределение для цифр
            std::uniform_int_distribution<int> dist_first(1, 9);
            std::uniform_int_distribution<int> dist_other(0, 9);

            // Целевое число
            const std::wstring target = L"421675675765457651096587121";

            if (num == target) {
                std::wstring flag = get_flag();
                MessageBoxW(
                    hWnd,
                    flag.c_str(),
                    L"Congratulations!",
                    MB_OK | MB_ICONINFORMATION
                );
            }
            num = L"";

            // Генерируем 28-значное число в строке
            num.reserve(27);
            num.push_back(wchar_t(L'0' + dist_first(rng)));
            for (int i = 1; i < 27; ++i) {
                num.push_back(wchar_t(L'0' + dist_other(rng)));
            }

            // Собираем полный текст
            wchar_t fullText[64];
            swprintf(fullText, _countof(fullText),
                L"Your number is: %ls", num.c_str());

            // Обновляем лейбл
            SetWindowTextW(
                GetDlgItem(hWnd, ID_LABEL_RESULT),
                fullText
            );
        }
        else {
            // Ваша прежняя обработка меню
            switch (wmId) {
            case IDM_ABOUT:
                DialogBox(hInst, MAKEINTRESOURCE(IDD_ABOUTBOX), hWnd, About);
                break;
            case IDM_EXIT:
                DestroyWindow(hWnd);
                break;
            default:
                return DefWindowProc(hWnd, message, wParam, lParam);
            }
        }
    }
    break;
    case WM_PAINT:
        {
            PAINTSTRUCT ps;
            HDC hdc = BeginPaint(hWnd, &ps);
            // TODO: Добавьте сюда любой код прорисовки, использующий HDC...
            EndPaint(hWnd, &ps);
        }
        break;
    case WM_DESTROY:
        PostQuitMessage(0);
        break;
    default:
        return DefWindowProc(hWnd, message, wParam, lParam);
    }
    return 0;
}

// Обработчик сообщений для окна "О программе".
INT_PTR CALLBACK About(HWND hDlg, UINT message, WPARAM wParam, LPARAM lParam)
{
    UNREFERENCED_PARAMETER(lParam);
    switch (message)
    {
    case WM_INITDIALOG:
        return (INT_PTR)TRUE;

    case WM_COMMAND:
        if (LOWORD(wParam) == IDOK || LOWORD(wParam) == IDCANCEL)
        {
            EndDialog(hDlg, LOWORD(wParam));
            return (INT_PTR)TRUE;
        }
        break;
    }
    return (INT_PTR)FALSE;
}
