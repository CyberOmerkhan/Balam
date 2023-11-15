using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Vacuume : MonoBehaviour
{

    public float speed = 1.5f;
    public bool moveLeft = true;
    void Start()
    {

    }

    void Update()
    {
        transform.Translate(Vector2.left * speed * Time.deltaTime);
    }

    public void Flip()
    {
        if (moveLeft == true)
        {
            moveLeft = false;
            transform.eulerAngles = new Vector3(0f, 180f, 0f);
        }
        else
        {
            moveLeft = true;
            transform.eulerAngles = new Vector3(0f, 0f, 0f);
        }
    }

    private void OnTriggerEnter2D(Collider2D collision)
    {
        if (collision.gameObject.tag == "flip")
        {
            Flip();
        }
    }
}
