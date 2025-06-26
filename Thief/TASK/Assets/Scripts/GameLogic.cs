using UnityEngine;
using UnityEngine.UI;

public class GameLogic : MonoBehaviour
{
    [SerializeField] private GameObject restartBtn;
    [SerializeField] private Text flagText;
    [SerializeField] private Text timerText;

    private string flag_text;

    private bool isWin = false;
    private float currentTime = 60;
    private int prevSecs;

    private string GetFlag()
    {
        string flag = "temp_var_for_flag";
        int[] codes = { 102, 108, 97, 103, 123, 117, 110, 49, 116, 121, 95, 36, 99, 114, 49, 112, 116, 95, 107, 49, 100, 100, 49, 51, 125 };
        char[] chars = new char[codes.Length];

        for (int i = 0; i < codes.Length; i++)
        {
            chars[i] = (char)codes[i];
        }

        return flag;
    }


    void UpdateTimerText(int seconds)
    {
        timerText.text = seconds.ToString();
        flag_text = GetFlag();
    }

    void Start()
    {
        Cursor.visible = false;

        UpdateTimerText((int)currentTime);
    }

    void Update()
    {
        transform.position = (Vector2)Camera.main.ScreenToWorldPoint(Input.mousePosition);

        if (currentTime > 0f)
        {
            currentTime -= Time.deltaTime;

            int seconds = Mathf.CeilToInt(currentTime);

            if (seconds != prevSecs)
            {
                prevSecs = seconds;
                UpdateTimerText(seconds);
            }
        }
        else
        {
            UpdateTimerText(0);
            isWin = true;
        }
    }

    private void OnTriggerEnter2D(Collider2D collision)
    {
        gameObject.SetActive(false);
        restartBtn.SetActive(true);
        Cursor.visible = true;
        if (isWin)
        {
            flagText.text = flag_text;
            flagText.gameObject.SetActive(true);
            timerText.gameObject.SetActive(false);
        }
        else
        {
            flagText.text = "Game Over";
            flagText.gameObject.SetActive(true);
            timerText.gameObject.SetActive(false);
        }
    }

    public void Restart()
    {
        Cursor.visible = false;
        isWin = false;
        currentTime = 60;
        flagText.gameObject.SetActive(false);
        timerText.gameObject.SetActive(true);
        restartBtn.SetActive(false);
        gameObject.SetActive(true);
    }
}
