import { createRouter, createWebHistory } from 'vue-router'
import ExhibitsView from '../views/ExhibitsView.vue';
import AuthorsView from '../views/AuthorsView.vue';
import CollectionsView from '../views/CollectionsView.vue';
import HallsView from '../views/HallsView.vue';
import ExhibitionsView from '../views/ExhibitionsView.vue';
import VisitorsView from '../views/VisitorsView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "ExhibitsView", 
      component: ExhibitsView
    },
    {
      path: "/authors",
      name: "AuthorsView", 
      component: AuthorsView
    },
    {
      path: "/collections",
      name: "CollectionsView", 
      component: CollectionsView
    },
    {
      path: "/halls",
      name: "HallsView", 
      component: HallsView
    },
    {
      path: "/exhibitions",
      name: "ExhibitionsView", 
      component: ExhibitionsView
    },
    {
      path: "/visitors",
        name: "VisitorsView", 
        component: VisitorsView
    }
  ]
})

export default router
