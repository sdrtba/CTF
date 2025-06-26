using UnityEngine;

public class EnemySpawner : MonoBehaviour
{
    [SerializeField] private GameObject entityPrefab;
    [SerializeField] private float spawnRate;

    private float timer;
    private Camera cam;

    void Start()
    {
        cam = Camera.main;
    }

    void Update()
    {
        timer += Time.deltaTime;
        if (timer >= spawnRate)
        {
            Spawn();
            timer = 0f;
        }
    }

    void Spawn()
    {
        Vector2 spawnPos = GetRandomEdgePosition();
        Vector2 targetPos = GetRandomScreenPosition();
        Vector2 direction = (targetPos - spawnPos).normalized;

        GameObject particle = Instantiate(entityPrefab, spawnPos, Quaternion.identity);
        particle.GetComponent<Entity>().SetDirection(direction);
    }

    Vector2 GetRandomEdgePosition()
    {
        float x, y;
        int side = Random.Range(0, 4);

        switch (side)
        {
            case 0: // Top
                x = Random.Range(0f, Screen.width);
                y = Screen.height + 50f;
                break;
            case 1: // Bottom
                x = Random.Range(0f, Screen.width);
                y = -50f;
                break;
            case 2: // Left
                x = -50f;
                y = Random.Range(0f, Screen.height);
                break;
            default: // Right
                x = Screen.width + 50f;
                y = Random.Range(0f, Screen.height);
                break;
        }

        return cam.ScreenToWorldPoint(new Vector3(x, y, 0f));
    }

    Vector2 GetRandomScreenPosition()
    {
        float x = Random.Range(0f, Screen.width);
        float y = Random.Range(0f, Screen.height);
        return cam.ScreenToWorldPoint(new Vector3(x, y, 0f));
    }
}
