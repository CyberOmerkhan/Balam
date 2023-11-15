using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Enemies : MonoBehaviour
{

    private void OnCollisionEnter2D(Collision2D collision)
    {
        if(collision.gameObject.tag == "Player")
        {
            print("asdasdaed");
            collision.gameObject.GetComponent<Player>().updateHP(-1);
        }
    }
}
