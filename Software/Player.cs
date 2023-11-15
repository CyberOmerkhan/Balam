using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Player : MonoBehaviour
{
    public float moveSpeed = 5f;
    public Rigidbody2D rb;
    Vector2 movement;
    public Animator animator;
    int curHP;
    int maxHP = 3;
    bool isHit = false;
    public bool key = false;
    bool canTp = true;
    public int coins = 0;
    public Main main;

    void Start()
    {
        curHP = maxHP;
        GetComponent<Rigidbody2D>().gravityScale = 0;
    }

    void Update()
    {
        movement.x = Input.GetAxisRaw("Horizontal");
        movement.y = Input.GetAxisRaw("Vertical");
        animator.SetFloat("Horizontal", movement.x);
        animator.SetFloat("Vertical", movement.y);
        animator.SetFloat("Speed", movement.sqrMagnitude);
    }

    void FixedUpdate()
    {
        rb.MovePosition(rb.position + movement * moveSpeed * Time.fixedDeltaTime);
    }

    public void updateHP(int x)
    {
        curHP += x;
        if (curHP > maxHP)
            curHP = maxHP;
        print(curHP);
        if (x < 0)
        {
            StopCoroutine(OnHit());
            isHit = true;
            StartCoroutine(OnHit());
        }
        if (curHP <= 0)
        {

            GetComponent<Rigidbody2D>().gravityScale = 70;
            GetComponent<CapsuleCollider2D>().enabled = false;
            Invoke("Lose", 1.5f);
        }
    }

    IEnumerator OnHit()
    {
        if(isHit)
            GetComponent<SpriteRenderer>().color = new Color(1f, GetComponent<SpriteRenderer>().color.g - 0.08f, GetComponent<SpriteRenderer>().color.b - 0.08f);
        else
            GetComponent<SpriteRenderer>().color = new Color(1f, GetComponent<SpriteRenderer>().color.g + 0.08f, GetComponent<SpriteRenderer>().color.b + 0.08f);

        if (GetComponent<SpriteRenderer>().color.g == 1)
            StopCoroutine(OnHit());
        else if(GetComponent<SpriteRenderer>().color.g <= 0)
        {
            isHit = false; ;
        }
        yield return new WaitForSeconds(0.08f);
        StartCoroutine(OnHit());
    }

    private void OnTriggerEnter2D(Collider2D collision)
    {
        if (collision.gameObject.tag == "Key")
        {
            Destroy(collision.gameObject);
            key = true;
        }
        else if (collision.gameObject.tag == "Door")
        {
            if (collision.gameObject.GetComponent<Door>().isOpen && canTp)
            {
                collision.gameObject.GetComponent<Door>().Teleport(gameObject);
                canTp = false;
                StartCoroutine(TPwait());
            }
            else if (key)
            {
                collision.gameObject.GetComponent<Door>().Unlock();
                if (canTp)
                {
                    collision.gameObject.GetComponent<Door>().Teleport(gameObject);
                    canTp = false;
                    StartCoroutine(TPwait());
                }
            }

        }
        else if (collision.gameObject.tag == "Water")
        {
            updateHP(-1);
        }
        else if (collision.gameObject.tag == "Heart")
        {
            updateHP(+1);
            Destroy(collision.gameObject);
        }
        else if (collision.gameObject.tag == "Coin"){
            coins++;
            print("Количество монет = " + coins);
            Destroy(collision.gameObject);
        }
    }

    IEnumerator TPwait()
    {
        yield return new WaitForSeconds(1f);
        canTp = true;
    }

    void Lose()
    {
        main.GetComponent<Main>().Lose();
    }

    public int getCoins()
    {
        return coins;
    }
    public int getHP(){
        return curHP;
    }
}

