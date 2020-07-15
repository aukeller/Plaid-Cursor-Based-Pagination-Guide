# Cursor-Based Pagination Guide

This step-by-step guide will demonstrate how to implement cursor-based pagination for the `/transactions/get` endpoint by sending a Retrieve Transactions request. We will be using the [Python Client Library](https://github.com/plaid/plaid-python), so the following code will be in Python.

## Background

Unlike offset pagination, cursor-based pagination works by returning a pointer to a specific item from a data set. Subsequent requests return results after the given pointer. The benefit of cursor-based pagination is that it scales well for large datasets, such as <span style="font-family:Courier">Transactions</span> associatied with an <span style="font-family:Courier">Item</span>, and handles real-time data effectively.

For offset pagination, a Retrieve Transactions request can look like this:

```python
    response = client.Transactions.get(access_token, 
                                       start_date='2020-01-01', 
                                       end_date='2020-06-01',
                                       count = 250, 
                                       offset = 1000)
``` 

The two optional fields provided here are `count` and `offset`, where `count` represents the number of transactions to fetch within a `start_date` and `end_date` window, and `offset` represents the number of transactions in the data set to skip over. In this case, the response from using offset pagination would skip over the first 1000 transactions in our set and return the following 250. The response would also return the total number of transactions. It would look like this: 

```
    >> http 200
    {
    "transactions": [...],
    "total_transactions": 1250
    }
```

Let's see how we can send the same request using cursor-based pagination. 

## Step #1: Sending a request

 When using cursor-based pagination, we can also utilize the optional `count` field, which functions the same way as before. However, instead of using the `offset` field, we will replace it with the `cursor` field, which represents where in the data set the next items should be fetched from.  When setting the `cursor` field to the value of `None` in a request, the response will default and return the first 250 transactions. For now, let's set this to `None` in our request:

```python
    response = client.Transactions.get(access_token, 
                                       start_date='2020-01-01', 
                                       end_date='2020-06-01',
                                       count = 250, 
                                       cursor = None)
``` 

## Step #2: Initial response

```
    >> http 200
    {
    "transactions": [...],
    "next_cursor": "eyJNYXJrZXIiOiBudWxsLCAiYm90b190cnVuY2F0ZV9hbW91bnQiOiAxfQ"
    }
```

Our response above returns an array of 250 transactions, which we previously specified with the `count` field in our request. More importantly though, our response returns a `next_cursor` attribute which points to the next item in our data set. 

## Step #3: Using `next_cursor`

Let's set the value of the `cursor` field in our subsequent request to the value of `next_cursor` from our previous response to return the next set of transactions:

```python
    response = client.Transactions.get(access_token, 
                                       start_date='2020-01-01', 
                                       end_date='2020-06-01',
                                       count = 250, 
                                       cursor = "eyJNYXJrZXIiOiBudWxsLCAiYm90b190cnVuY2F0ZV9hbW91bnQiOiAxfQ")
```

## Step #4: Successful pagination

```
    >> http 200
    {
    "transactions": [...],
    "next_cursor": ""
    }
```

Now our response returns the next 250 transactions, starting with the item that falls after the new cursor we set. This illustrates how we can successfully paginate using a cursor-based approach by returning results after the `next_cursor` in each response. 

Notice that this time our `next_cursor` attribute has an empty-string value. An empty-string value simply means that we have reached the end of our data set. 

## Conclusion

Though cursor-based pagination has its benefits over offset pagination, it comes with some drawbacks:  

* It assumes that we are working with a unique, sequential set of data, which may not always be the case 

* Unlike offset pagination, we cannot jump to a specific page of our transactions

* There is no concept of the total number of transactions that are normally returned with offset pagination


However, cursor-based pagination is becoming more popular because we don't have to see any transactions in our data set we've already visited, and we don't need to return the total number of transactions all at once. Using cursor-based pagination also means that we can work with large data sets that may change frequently.



