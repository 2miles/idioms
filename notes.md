## This will define the origin_components table

```sql
CREATE TABLE idiom_origin_test (
    origin_id SERIAL PRIMARY KEY,
    idiom_id INT NOT NULL UNIQUE,
    origin TEXT,
    FOREIGN KEY (idiom_id) REFERENCES idioms_test (id)
);
```

## This will define the idiom_examples_test table

```sql
CREATE TABLE idiom_examples_test (
    example_id SERIAL PRIMARY KEY,
    idiom_id INT NOT NULL,
    example TEXT,
    FOREIGN KEY (idiom_id) REFERENCES idioms_test (id)
);
```

## This will need to be updated to fetch all the origin components for each idiom.

```tsx
// Get single idiom, and get examples for that idiom
// Route for handling HTTP GET requests to /api/v1/idioms/:id
// Return the added idiom, and its examples in the response
app.get('/api/v1/idioms/:id', async (req, res) => {
  try {
    const idiomQuery = await pool.query(
      ` SELECT * FROM idioms_test WHERE id = $1 `,
      [req.params.id],
    );
    const examplesQuery = await pool.query(
      `SELECT * FROM idiom_examples_test WHERE idiom_id = $1`,
      [req.params.id],
    );
    // right here it will go
    res.status(200).json({
      status: 'success',
      data: {
        idiom: idiomQuery.rows[0],
        examples: examplesQuery.rows,
        // right here too
      },
    });
  } catch (error) {
    console.error('Error executing query:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});
```

## This will be the fetchData useEffect in DetailPage.tsx

```tsx
useEffect(() => {
  const fetchData = async () => {
    try {
      const response = await IdiomFinder.get(`/${id}`);
      setSelectedIdiom(response.data.data.idiom);
      setExamples(response.data.data.examples);
      setOrigin(response.data.data.origin); // New
      setLoading(false);
    } catch (err) {
      console.log(err);
      setLoading(false);
    }
  };
  fetchData();
}, [id, setSelectedIdiom]);
```

## I dont think im going to use this fetch function. I think im going to put the Origin text directly into the DetailPage.tsx and not in its own component. But this gives me an idea on how to render it.

```tsx
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './styles.css'; // Import the CSS file

const IdiomComponent = ({ idiomId }) => {
  const [components, setComponents] = useState([]);

  useEffect(() => {
    const fetchComponents = async () => {
      try {
        const response = await axios.get(`/api/idioms/${idiomId}/components`);
        setComponents(response.data);
      } catch (error) {
        console.error('Error fetching idiom components:', error);
      }
    };

    fetchComponents();
  }, [idiomId]);

  return (
    <div>
      {components.map((component) => {
        if (component.component_type === 'paragraph') {
          return <p key={component.sequence}>{component.content}</p>;
        } else if (component.component_type === 'blockquote') {
          return (
            <blockquote key={component.sequence}>
              {component.content}
            </blockquote>
          );
        } else if (component.component_type === 'title') {
          return (
            <span key={component.sequence} className="title">
              {component.content}
            </span>
          );
        } else {
          return null; // Handle unexpected types or errors
        }
      })}
    </div>
  );
};

export default IdiomComponent;
```
