import React, { useEffect, useState } from "react";
import "./App.css";

import { Container } from "@material-ui/core";
import Card from "@material-ui/core/Card";

import Header from "./Components/Header";
import Tasks from "./Components/Tasks";
import TaskForm from "./Components/TaskForm";


function App() {
  // Once we get data from the api, we transfer it into state
  const [tasks, setTasks] = useState([]);
  // const [searchTasks, setSearchTasks] = useState([]);
  // Make Api call to Flask Server and render tasks (React Hooks)
  // Only called when component first mounts
  // URL is set in package.json with a Proxy (to prevent problems with CORS)
  // UseEffect cannot use async/await
  useEffect(() => {
    fetch("http://54.88.155.50:5000/getTasks").then((response) =>
      response.json().then((data) => {
        setTasks(data.tasks);
      })
    );
  }, []);

  return (
    <div className="App">
      <Header></Header>
      <Container maxWidth="md" style={{ marginBottom: 16 }}>
        <TaskForm
          // Add created task to state list
          // Prop passed in to the task, called whenever there is a new task
          onNewTask={(taskToAdd) =>
            // Adding new task onto the end (opposite order to add to start)
            setTasks((currentTasks) => [...currentTasks, taskToAdd])
          }
        ></TaskForm>
        <Card>
          <Tasks
            // tasks={chooseTaskList(tasks, searchTasks)}
            tasks={tasks}
            Find the task that has been edited and update state list
            onEditTask={(task) => {
              setTasks(
                tasks.map((item) => {
                  // Edited task found
                  if (item.id === task.id) {
                    return task;
                  } else {
                    return item;
                  }
                })
              );
            }}
            onDeleteTask={(task) =>
              setTasks((currentTasks) => [
                ...currentTasks.filter((x) => x !== task),
              ])
            }
          />
        </Card>
      </Container>
    </div>
  );
}

export default App;
