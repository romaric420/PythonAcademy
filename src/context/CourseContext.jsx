import { createContext, useContext, useState, useEffect } from "react";
import { UNLOCK_CODE } from "../data/courseData";

const CourseContext = createContext();

export function CourseProvider({ children }) {
  const [isFullyUnlocked, setIsFullyUnlocked] = useState(() => {
    return localStorage.getItem("pa_code_entered") === "true";
  });

  const [completedCourses, setCompletedCourses] = useState(() => {
    const saved = localStorage.getItem("pa_completed");
    return saved ? JSON.parse(saved) : {};
  });

  useEffect(() => {
    localStorage.setItem("pa_completed", JSON.stringify(completedCourses));
  }, [completedCourses]);

  const enterCode = (code) => {
    if (code === UNLOCK_CODE) {
      setIsFullyUnlocked(true);
      localStorage.setItem("pa_code_entered", "true");
      return true;
    }
    return false;
  };

  const resetAccess = () => {
    setIsFullyUnlocked(false);
    setCompletedCourses({});
    localStorage.removeItem("pa_code_entered");
    localStorage.removeItem("pa_completed");
  };

  // First course of each level = free. Rest = locked unless code entered.
  const isCourseAccessible = (levelId, courseIndex) => {
    if (isFullyUnlocked) return true;
    return courseIndex === 0; // Only first course is free
  };

  // Levels: always accessible (user can enter and see course list)
  // but individual courses are locked (except first)
  const isLevelAccessible = () => true;

  const markComplete = (levelId, courseId) => {
    setCompletedCourses((prev) => ({
      ...prev,
      [`${levelId}-${courseId}`]: true,
    }));
  };

  const isCourseCompleted = (levelId, courseId) => {
    return completedCourses[`${levelId}-${courseId}`] || false;
  };

  const getProgress = (levelId, courses) => {
    if (!courses || courses.length === 0) return 0;
    const completed = courses.filter((c) => completedCourses[`${levelId}-${c.id}`]).length;
    return Math.round((completed / courses.length) * 100);
  };

  return (
    <CourseContext.Provider
      value={{
        isFullyUnlocked,
        completedCourses,
        enterCode,
        resetAccess,
        isCourseAccessible,
        isLevelAccessible,
        markComplete,
        isCourseCompleted,
        getProgress,
      }}
    >
      {children}
    </CourseContext.Provider>
  );
}

export const useCourse = () => useContext(CourseContext);
