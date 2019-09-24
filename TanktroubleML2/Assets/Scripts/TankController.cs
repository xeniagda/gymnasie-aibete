using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TankController : MonoBehaviour
{

    public GameObject shot;



    Rigidbody rb;
    float angle;
    public float spd;
    public float turnSpd;

    public string forward;
    public string backward;
    public string left;
    public string right;
    public string shoot;
    


    // Start is called before the first frame update
    void Start()
    {
        rb = GetComponent<Rigidbody>();
    }

    // Update is called once per frame
    void Update()
    { 
        if (Input.GetKeyDown(shoot))
            Shoot();


        if (Input.GetKey(left))
            angle -= Time.deltaTime * turnSpd * 40f;
        if (Input.GetKey(right))
            angle += Time.deltaTime * turnSpd * 40f;
        
        Quaternion rot = Quaternion.AngleAxis(angle, transform.up);
        rb.MoveRotation(rot);
        if (Input.GetKey(forward))
            rb.MovePosition(transform.position + transform.forward * spd * Time.deltaTime);
        if (Input.GetKey(backward))
            rb.MovePosition(transform.position - transform.forward * spd * Time.deltaTime);

        Halt();
    }

    void OnCollisionEnter(Collision coll) {
        if (coll.gameObject.tag == "wall")
            rb.velocity = new Vector3(0f, 0f, 0f);
        
        if (coll.gameObject.tag == "shot")
            Die();
        
    }
    void Die() {
        Debug.Log("You Died");

    }

    void Halt() {
        if (Input.GetAxis("Horizontal") + Input.GetAxis("Vertical") == 0.0f)
        {
            rb.velocity = new Vector3(0f, 0f, 0f);
            
        }
    }

    void Shoot() {
        Instantiate(shot, transform.position + transform.forward * transform.localScale.z, transform.rotation);

    }
}
